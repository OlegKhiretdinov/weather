from weather.database import Session
from weather.models import User, Location, SearchHistory
from sqlalchemy import select, func


def add_user_query():
    with Session() as session:
        user = User()
        session.add(user)
        session.flush()
        user_id = user.uid
        session.commit()
    return user_id


def add_location_query(loc_id, name, lat, long):
    with Session() as session:
        with session.begin():
            session.add(Location(id=loc_id, name=name, latitude=lat, longitude=long))


def add_history_entry_query(uid, loc_id):
    with Session() as session:
        with session.begin():
            session.add(SearchHistory(user_id=uid, location_id=loc_id))


def get_location_query(loc_id):
    with Session() as session:
        location = session.query(Location).get(loc_id)
    return location


def get_user_query(uid):
    with Session() as session:
        user = session.query(User).get(uid)
    return user


def get_last_user_location_query(uid):
    with Session() as session:
        location_id_query = select(SearchHistory.location_id)\
            .where(SearchHistory.user_id == uid)\
            .order_by(SearchHistory.created_at.desc()).limit(1).scalar_subquery()
        query = select(Location.id, Location.name).where(Location.id == location_id_query)
        data = session.execute(query).fetchone()
    return data


def get_user_statistic(uid):
    with Session() as session:
        query = select(Location.name, Location.id, func.count(SearchHistory.location_id))\
            .join(SearchHistory, Location.id == SearchHistory.location_id)\
            .where(SearchHistory.user_id == uid)\
            .group_by(Location.id)\
            .order_by(func.count(SearchHistory.location_id).desc())
        data = session.execute(query).all()
    return data


def get_user_history(uid):
    with Session() as session:
        query = select(Location.name, SearchHistory.created_at)\
            .join(SearchHistory, Location.id == SearchHistory.location_id)\
            .where(SearchHistory.user_id == uid)\
            .order_by(SearchHistory.created_at.desc())
        data = session.execute(query).all()
    return data
