from datetime import datetime

from db.pg_base import PostgresService
from models.user import User, Role, UserRole
from sqlalchemy.orm import Session


class UserService(PostgresService):
    def __init__(self):
        super().__init__()

    def add_role(self, name, description):
        with Session(self.engine) as session:
            role = session.query(Role).filter(Role.name == name).one()
            if role:
                return False

            added_role = Role()
            added_role.name = name
            added_role.description = description

            session.add(added_role)
            session.commit()

            return True

    def del_role(self, role_id):
        with Session(self.engine) as session:
            role = session.query(Role).filter(Role.id == role_id).one()
            if not role:
                return False

            session.query(Role).filter(Role.id == role_id).delete()

            return True

    def update_role(self, role_id, name, description):
        with Session(self.engine) as session:
            role = session.query(Role).filter(Role.id == role_id).one()
            if not role:
                return False

            session.query(Role).filter(Role.id == role_id).delete()

            updated_role = Role()
            updated_role.id = role_id
            updated_role.name = name
            updated_role.description = description
            updated_role.modified = datetime.utcnow()

            session.add(updated_role)
            session.commit()

            return True

    def show_roles(self):
        with Session(self.engine) as session:
            data = session.query(Role).all()
            return data

    def user_add_role(self, user_id, role_id):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).one()
            role = session.query(Role).filter(Role.id == role_id).one()
            if not user or not role:
                return False

            user_add_role = UserRole()
            user_add_role.user_id = user_id
            user_add_role.role_id = role_id

            session.add(user_add_role)
            session.commit()

            return True

    def user_remove_role(self, user_id, role_id):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).one()
            role = session.query(Role).filter(Role.id == role_id).one()
            user_role = session.query(UserRole). \
                filter(UserRole.user_id == user_id,
                       UserRole.role_id == role_id).one()
            if not user or not role or not user_role:
                return False

            session.query(UserRole).filter(UserRole.id == user_role.id).delete()

            return True

    def user_check_role(self, user_id, role_id):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).one()
            role = session.query(Role).filter(Role.id == role_id).one()
            user_role = session.query(UserRole). \
                filter(UserRole.user_id == user_id,
                       UserRole.role_id == role_id).one()
            if not user or not role or not user_role:
                return False

            return True
