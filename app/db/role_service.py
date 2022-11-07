from datetime import datetime

from db.pg_base import PostgresService
from models.user import User, Role, UserRole
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


class RoleService(PostgresService):
    def __init__(self):
        super().__init__()

    def add_role(self, name, description):
        with Session(self.engine) as session:
            try:
                role = session.query(Role).filter(Role.name == name).one()
                if role:
                    return False
            except NoResultFound:
                added_role = Role()
                added_role.name = name
                added_role.description = description

                session.add(added_role)
                session.commit()

                return True

    def del_role(self, role_id):
        # TODO: not working
        with Session(self.engine) as session:
            try:
                session.query(Role).filter(Role.id == role_id).delete()
                return True
            except NoResultFound:
                return False

    def update_role(self, role_id, name, description):
        with Session(self.engine) as session:
            try:
                role = session.query(Role).filter(Role.id == role_id).one()
                session.query(Role).filter(Role.id == role_id).delete()
                updated_role = Role()
                updated_role.id = role_id
                if name:
                    updated_role.name = name
                if description:
                    updated_role.description = description
                if name or description:
                    updated_role.modified = datetime.utcnow()
                session.add(updated_role)
                session.commit()
                return True
            except NoResultFound:
                return False

    def show_all_roles(self):
        with Session(self.engine) as session:
            return session.query(Role).all()

    def show_role(self, role_id):
        with Session(self.engine) as session:
            try:
                return session.query(Role).filter(Role.id == role_id).all()
            except NoResultFound:
                return False

    def user_add_role(self, user_id, role_id):
        with Session(self.engine) as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
            except NoResultFound:
                return False
            try:
                role = session.query(Role).filter(Role.id == role_id).one()
            except NoResultFound:
                return False

            if user_id and role_id:
                user_add_role = UserRole()
                user_add_role.user_id = user_id
                user_add_role.role_id = role_id

                session.add(user_add_role)
                session.commit()

                return True

    def user_remove_role(self, user_id, role_id):
        # TODO: delete relationships objects
        with Session(self.engine) as session:
            if not user_id or not role_id:
                return False

            try:
                user = session.query(User).filter(User.id == user_id).one()
            except NoResultFound:
                return False
            try:
                role = session.query(Role).filter(Role.id == role_id).one()
            except NoResultFound:
                return False
            user_role = session.query(UserRole). \
                filter(UserRole.user_id == user_id,
                       UserRole.role_id == role_id).one()

            if not user or not role or not user_role:
                return False

            session.query(UserRole).filter(UserRole.id == user_role.id).delete()

            return True

    def user_check_role(self, user_id, role_id):
        with Session(self.engine) as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
            except NoResultFound:
                return False
            try:
                role = session.query(Role).filter(Role.id == role_id).one()
            except NoResultFound:
                return False

            try:
                user_role = session.query(UserRole).filter(
                    UserRole.user_id == user_id,
                    UserRole.role_id == role_id).one()
                return True
            except NoResultFound:
                return False

