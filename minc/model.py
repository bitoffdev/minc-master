import secrets

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://rms:password@localhost/minc", echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), index=True)
    pass_hash = Column(String(128))
    token = Column(String(32), index=True)

    def __repr__(self):
        return "<User(id='%s' email='%s', pass_hash='%s')>".format(
            self.id, self.email, self.password
        )


# ensure that the tables exist
Base.metadata.create_all(engine)


def create_user(email, password):
    """
    create a user with the given email and password
    """
    pass_hash = generate_password_hash(password)
    token = secrets.token_hex(16)
    user = User(email=email, pass_hash=pass_hash, token=token)
    session.add(user)
    session.commit()
    return user


def get_user(email, password):
    for user in session.query(User).filter(User.email == email):
        if check_password_hash(user.pass_hash, password):
            user.token = secrets.token_hex(16)
            session.add(user)
            session.commit()
            return user
    return None
