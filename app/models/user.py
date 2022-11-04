from ast import Str
import datetime

from email.policy import default
from enum import unique
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


#from config.settings import Settings


db_connection_string = 'postgresql+psycopg2://user:123qwe@0.0.0.0:5432/db_users'
engine = create_engine(
    db_connection_string,
    isolation_level = "REPEATABLE READ",
    echo=True,
)

Base = declarative_base()
#settings = Settings()
#meta = MetaData()

# class User(Base):
#     __tablename__ = "user_account"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String(30), unique=True, nullable=False)
#     first_name = Column(String(30), nullable=True, default='First Name')
#     last_name = Column(String(50), nullable=True, default='Last Name')
#     password = Column(String, nullable=False)
#     #verified_email = Column(Boolean, default=True)
#     date_joined = Column(DateTime, default=datetime.datetime.utcnow())
#     is_active = Column(Boolean, default=True)
#     # agent_id = Column(Integer, ForeignKey('user_agent.id'))
#
#     #agent = relationship('UserAgent', back_populates='user') # 1
#
#     #firstname = Column(String, default='NONAME')
#     # addresses = relationship(
#     #     "Address", back_populates="user", cascade="all, delete-orphan"
#     # )
#     def __repr__(self):
#         return f"User(id={self.id!r}, email={self.email!r}, password={self.password!r})"


class LoginRecord(Base):
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_time = Column(DateTime(), nullable=False)
    useragent = Column(String(256), nullable=True)

    userinfo_id = Column(Integer, ForeignKey('user_info.id'), nullable=False)

class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), unique=True, nullable=False)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    password = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    login_records = relationship('LoginRecord')
    roles = relationship('User_Role', backref='userinfo')

class User_Role(Base):
    __tablename__ = 'user__role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userinfo_id = Column(Integer(), ForeignKey('user_info.id'))
    role_id = Column(Integer(), ForeignKey('role.id'))

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    users = relationship('User_Role', backref='role')

class Resource_Role(Base):
    __tablename__ = 'resource__role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer(), ForeignKey('role.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    can_create = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_update = Column(Boolean, nullable=False)
    can_delete = Column(Boolean, nullable=False)





# class UserAgent(Base):
#     __tablename__ = "user_agent"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_agent = Column(String, default='Some User Agent')
#     auth_history = Column(String, default=datetime.datetime.now())
#     refresh_token = Column(String, default='some refresh_token')
#     user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
#     user = relationship("User", back_populates="agent") # 1





Base.metadata.create_all(bind=engine)

# Пользовательскими данными считаются id, username,
# email, password, last_name, first_name, а служебными — is_staff, is_active, is_superuser, last_login, date_joined


# id,
# user_id (связь с таблицей пользователей),
# user_agent, или более подробный fingerprint,
# дата аутентификации,
# другая информация о входе




# user = Table('Users', meta,
#              Column('id', Integer, primary_key=True),
#              Column('email', Integer, primary_key=True),
#              Column('password', Integer, primary_key=True)
# )

# class Address(Base):
#     __tablename__ = "address"
#     id = Column(Integer, primary_key=True)
#     email_address = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
#     user = relationship("User", back_populates="addresses")
#     def __repr__(self):
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
