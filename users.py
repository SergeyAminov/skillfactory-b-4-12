import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Указание пути к БД
# (файл базы должен находиться в одной директории с данным модулем)
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


class User(Base):

    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Integer)


def request_data():
    first_name = input("Name: ")
    last_name = input("Surname: ")
    gender = input("Gender: ")
    email = input("Email: ")
    birthdate = input("Birthday: ")
    height = input("Height: ")

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()


if __name__ == '__main__':
    main()
