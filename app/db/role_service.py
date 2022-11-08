from datetime import datetime

from db.pg_base import PostgresService
from models.user import User, Role, UserRole
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from werkzeug.exceptions import HTTPException, BadRequest


class RoleService(PostgresService):
    def __init__(self):
        super().__init__()

    def add_role(self, name, description):
        with Session(self.engine) as session:
            if not name:
                raise BadRequest(description=f'''field 'name' must be specified''')
            try:
                role = session.query(Role).filter(Role.name == name).one()
                if role:
                    raise BadRequest(description=f'''Role with name={name} exist''')
            except NoResultFound:
                added_role = Role()
                added_role.name = name
                added_role.description = description

                session.add(added_role)
                session.commit()

                return f'''Role name={name}, description={description if description else '<not specified>'} created'''

    def del_role(self, role_id):
        with Session(self.engine) as session:
            try:
                session.query(Role).filter(Role.id == role_id).delete()
                session.commit()
                return f'''Role with id={role_id} deleted'''
            except NoResultFound:
                raise BadRequest(description=f'''Role with id={role_id} doesn't exist''')

    def update_role(self, role_id, name, description):
        with Session(self.engine) as session:
            try:
                session.query(Role).filter(Role.id == role_id).one()
            except NoResultFound:
                raise BadRequest(description=f'''Role with id={role_id} doesn't exist''')

            if not name and not description:
                raise BadRequest(description=f'''Nothing to update''')
            elif not name:
                session.query(Role).filter(Role.id == role_id).update(
                    {'description': description, 'modified': datetime.utcnow()}
                )
                session.commit()
            elif not description:
                session.query(Role).filter(Role.id == role_id).update(
                    {'name': name, 'modified': datetime.utcnow()}
                )
                session.commit()
            else:
                session.query(Role).filter(Role.id == role_id).update(
                    {'name': name, 'description': description, 'modified': datetime.utcnow()}
                )
                session.commit()

            return f'Role updated, for id={role_id} new values name={name if name else "<not specified>"}, ' \
                   f'description={description if description else "<not specified>"}'

    def show_all_roles(self):
        with Session(self.engine) as session:
            return session.query(Role).all()

    def show_role(self, role_id):
        with Session(self.engine) as session:
            try:
                return session.query(Role).filter(Role.id == role_id).all()
            except NoResultFound:
                raise BadRequest(description=f'''Role with id={role_id} doesn't exist''')

    def user_add_role(self, user_id, role_id):
        with Session(self.engine) as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
            except NoResultFound:
                raise BadRequest(description=f'''User with id={user_id} doesn't exist''')

            try:
                role = session.query(Role).filter(Role.id == role_id).one()
            except NoResultFound:
                raise BadRequest(description=f'''Role with id={role_id} doesn't exist''')

            try:
                user_role = session.query(UserRole).filter(UserRole.user_id == user_id,
                                                           UserRole.role_id == role_id).one()
                raise BadRequest(description=f'''UserRole with User.id={user_id}, Role.id={role_id} exist''')
            except MultipleResultsFound:
                raise BadRequest(description=f'''UserRole with User.id={user_id}, Role.id={role_id} multiple exist''')
            except NoResultFound:
                user_add_role = UserRole()
                user_add_role.user_id = user_id
                user_add_role.role_id = role_id
                session.add(user_add_role)
                session.commit()
                return f'user_role row with user_id={user_id}, role_id={role_id} created'

    def user_remove_role(self, user_id, role_id):
        with Session(self.engine) as session:
            if not user_id or not role_id:
                raise BadRequest(description=f''''user_id' and 'role_id' must be specified''')

            try:
                user_role = session.query(UserRole). \
                    filter(UserRole.user_id == user_id,
                           UserRole.role_id == role_id).one()
                session.query(UserRole).filter(UserRole.id == user_role.id).delete()
                session.commit()
                return f'UserRole with id={user_role.id} deleted'
            except NoResultFound:
                raise BadRequest(
                    description=f'''UserRole with 'user_id'={user_id}, 'role_id'={role_id} doesn't exist''')

    def user_check_role(self, user_id, role_id):
        with Session(self.engine) as session:
            # try:
            #     user = session.query(User).filter(User.id == user_id).one()
            # except NoResultFound:
            #     raise BadRequest(description=f'''User with id={user_id} doesn't exist''')
            #
            # try:
            #     role = session.query(Role).filter(Role.id == role_id).one()
            # except NoResultFound:
            #     raise BadRequest(description=f'''Role with id={role_id} doesn't exist''')
            # TODO: это надо убрать, но нужно сделать каскадное удаление в таблице user__role при удалении user или role соответствующих

            try:
                user_role = session.query(UserRole).filter(
                    UserRole.user_id == user_id,
                    UserRole.role_id == role_id).one()
                return user_role
            except NoResultFound:
                raise BadRequest(
                    description=f'''user_role row with user_id={user_id}, role_id={role_id} doesn't exist''')

    def user_role_show_all(self):
        with Session(self.engine) as session:
            return session.query(UserRole).all()