import os

from flask import Flask, render_template, request
from psycopg2 import errors
from sqlalchemy import exc

from weather.queries import add_location_query, add_history_entry_query, get_location_query, \
    get_last_user_location_query, get_user_statistic, get_user_history
from weather.utils import check_current_user_id
from weather.weather_api import search_location, get_weather

app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY')


@app.get('/')
def home_page():
    user_id, is_new_user = check_current_user_id()
    search_str = request.values.get('location')

    if not is_new_user and not search_str:
        # Смотрим последний город в истории пользователя
        last_location = get_last_user_location_query(user_id)

    if not search_str or len(search_str) < 2:
        #  Для поиска нужно больше двух символов
        return render_template(
            'pages/home_page.html',
            search_str=search_str,
            last_location=last_location
        )
    else:
        locations_data = search_location(search_str)
        return render_template(
            'pages/home_page.html',
            locations=locations_data,
            search_str=search_str,
        )


@app.route('/weather/<int:location_id>', methods=['POST', 'GET'])
def weather(location_id):
    user_id, _ = check_current_user_id()
    # Получаем координаты города для запросы погоды
    try:
        if request.method == 'POST':
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            name = request.form['name']

        if request.method == 'GET':
            location = get_location_query(location_id)
            latitude = location.latitude
            longitude = location.longitude
            name = location.name
    except (AttributeError, KeyError):
        return render_template(
            'pages/weather.html',
            error=True
        )
    # Запрос прогноза
    data, status = get_weather(latitude, longitude)

    if status == 200 and request.method == 'POST':
        try:
            # пробуем добавить город в базу
            add_location_query(location_id, name, latitude, longitude)
        except exc.IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                pass
            else:
                raise
    # Запись о запросе в историю
    add_history_entry_query(user_id, location_id)

    return render_template(
        'pages/weather.html',
        location=name,
        weather_data=data.get('daily'),
        error=data.get('error', False)
    )


@app.get('/statistic')
def statistic():
    user_id, _ = check_current_user_id()
    data = get_user_statistic(user_id)

    return render_template('pages/statistic.html', statistic=data)


@app.get('/history')
def history():
    user_id, _ = check_current_user_id()
    data = get_user_history(user_id)

    return render_template('pages/history.html', history=data)


@app.template_filter('formatdatetime')
def format_datetime(value, format_tmp="%d/%m/%y %H:%M"):
    if value is None:
        return ""
    return value.strftime(format_tmp)
