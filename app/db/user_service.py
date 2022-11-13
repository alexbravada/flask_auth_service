from db.pg_base import PostgresService
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort


class UserService(PostgresService):
    def __init__(self):
        super().__init__()

    def register(self, email, password):
        with Session(self.engine) as session:
            try:
                user = session.query(User).filter(User.email == email).one()
                if user:
                    abort(400)
            except MultipleResultsFound as e:
                abort(400)
            except NoResultFound as e:
                user = User(email=email, password=generate_password_hash(password))
                session.add(user)
                session.commit()
                user = session.query(User).filter(User.email == email).one()
                return user

    def login(self, email, password):
        with Session(self.engine) as session:
            user = 'NO USER'
            try:
                # user = session.query(User.email==email).one()
                user = session.query(User).filter(User.email == email).one()
                print(user, "!!!!!!!!!!!!!!!!")
                print('abssssssssssssssssssssssssssssssssssssssss\n\n\n\n\n\n\n\n\n')
                if user:
                    if check_password_hash(user.password, password):
                        return True
                return False
            except NoResultFound as ee:
                print('\n\n\n\n', ee, '\n\n\n\n\n', user)
                return False
