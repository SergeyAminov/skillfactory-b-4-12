import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    """
    Создание соединения с БД
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def convert_to_datetime(date_str):
    """
    Возвращает преобразованную строку даты в объект datetime
    """
    date_str_list = date_str.split('-')
    date_list = map(int, date_str_list)
    date = datetime.date(*date_list)
    return date


def get_user(user_id, session):
    """
    Возвращает пользователя по указанному ID
    """
    user = session.query(User).filter(User.id == int(user_id)).first()
    return user


def find_nearest(user, session):
    """
    Возвращает двух "ближайших" атлетов к данному поьзователю
    """
    user_birthdate = convert_to_datetime(user.birthdate)
    athletes = session.query(Athlete).all()

    nearest_birthdate_athlete = None
    nearest_height_athlete = None
    height_abs = None
    birthdate_abs = None

    for athlete in athletes:

        if athlete.height is not None:

            if height_abs is not None:
                if height_abs > abs(user.height - athlete.height):
                    height_abs = abs(user.height - athlete.height)
                    nearest_height_athlete = athlete
            else:
                height_abs = abs(user.height - athlete.height)
                nearest_height_athlete = athlete

        if athlete.birthdate is not None:

            athlete_birthdate = convert_to_datetime(athlete.birthdate)

            if birthdate_abs is not None:
                if birthdate_abs > abs(user_birthdate - athlete_birthdate):
                    birthdate_abs = abs(user_birthdate - athlete_birthdate)
                    nearest_birthdate_athlete = athlete
            else:
                birthdate_abs = abs(user_birthdate - athlete_birthdate)
                nearest_birthdate_athlete = athlete

    return nearest_height_athlete, nearest_birthdate_athlete


def main():
    session = connect_db()
    user_id = input('Please input user ID: ')
    user = get_user(user_id, session)
    if not user:
        print('User was not found.')
    else:
        athletes = find_nearest(user, session)
        print('Nearest athlete by height: {athlete_name}, {athlete_height}'
              .format(athlete_name=athletes[0].name, athlete_height=athletes[0].height))

        print('Nearest athlete by birthdate: {athlete_name}, {athlete_birthdate}'
              .format(athlete_name=athletes[1].name, athlete_birthdate=athletes[1].birthdate))


if __name__ == '__main__':
    main()
