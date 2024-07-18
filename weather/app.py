from flask import Flask, render_template, request

from .api import search_location, get_weather

app = Flask(__name__)


@app.get('/')
def home_page():
    search_str = request.values.get('location')
    if not search_str:
        return render_template('pages/home_page.html')
    elif len(search_str) < 2:
        #  Для поиска нужно больше двух символов
        return render_template(
            'pages/home_page.html',
            locations=[],
            search_str=search_str
        )
    else:
        locations_data = search_location(search_str)
        return render_template(
            'pages/home_page.html',
            locations=locations_data,
            search_str=search_str
        )


@app.route('/weather/<int:location_id>', methods=['POST', 'GET'])
def weather(location_id):
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        name = request.form.get('name')

    data = get_weather(latitude, longitude)
    return render_template(
        'pages/weather.html',
        location=name,
        units=data.get('daily_units'),
        weather_data=data.get('daily'),
        error=data.get('error', False)
    )
