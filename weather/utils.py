from flask import session

from weather.queries import get_user_query, add_user_query


def check_current_user_id():
    """
    Возвращает кортеж из двух значений:
    1.uid пользователя. Если в session нет id или session.id нет в бд,
    то создаётся новый пользователь.
    2.Флаг определяет новый пользователь или нет
    :return: (uid, is_new_user)
    """
    is_new_user = False
    user = get_user_query(session.get('user_id'))
    user_id = user and user.uid

    if not user_id:
        user_id = add_user_query()
        session['user_id'] = user_id
        is_new_user = True

    return user_id, is_new_user
