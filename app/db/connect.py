
from models.user import User
from config.settings import Settings

from sqlalchemy import create_engine
from sqlalchemy import select

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound


from werkzeug.security import generate_password_hash, check_password_hash




# db_connection_string = 'postgresql+psycopg2://user:123qwe@0.0.0.0:5432/db_users'
# engine = create_engine(
#     db_connection_string,
#     isolation_level = "REPEATABLE READ",
#     echo=True,
# )

#settings = Settings()

class PostgresService:
    def __init__(self):
        self.settings = Settings()
        self.engine = create_engine(
                                self.settings.PG_CONNECT_STRING,
                                isolation_level = "REPEATABLE READ",
                                echo=True
                            )
        #self.engine = self.settings.PG_ENGINE
        
    def register(self, email, password):
        with Session(self.engine) as session:
            try:
                user = session.query(User).filter(User.email==email).one()
                print(f'\n\n\n\n\nUSER {user}\n\n\n')
                if user:
                    return {"status": "403", "msg": "account with that email has been used"}
            except MultipleResultsFound as e:
                print(e)
                return {"status": "403", "msg": "account with that email has been used"}
            except NoResultFound as e:
                print(e)
                print('email not registered')
                user = User(email=email, password=generate_password_hash(password))
                session.add(user)
                session.commit()
            print('after commit')
            return {"status":"201"}

    
    def login(self, email, password):
        with Session(self.engine) as session:
            user = 'NO USER'
            try:
                #user = session.query(User.email==email).one()
                user = session.query(User).filter(User.email==email).one()
                print(user, "!!!!!!!!!!!!!!!!")
                print('abssssssssssssssssssssssssssssssssssssssss\n\n\n\n\n\n\n\n\n')
                if user:
                    if check_password_hash(user.password, password):
                        return True
                return False
            except NoResultFound as ee:
                print('\n\n\n\n', ee, '\n\n\n\n\n', user)
                return False
