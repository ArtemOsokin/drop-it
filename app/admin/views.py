from typing import List, Type

from sqladmin import ModelView
from wtforms import Form
from wtforms.fields.simple import PasswordField

from app.core.security import AuthUtils
from app.models import User, Drop, Genre


class UserAdmin(ModelView, model=User):
    name = 'User'
    name_plural = 'Users'

    column_labels = {User.hashed_password: "password"}
    column_list = [User.id, User.username, User.email, User.is_admin]
    column_searchable_list = [User.username, User.first_name, User.last_name, User.email]
    column_sortable_list = [User.username, User.first_name, User.last_name, User.email]
    column_default_sort = [(User.username, True)]
    column_filterable_list = [User.is_admin]

    form_excluded_columns = ['hashed_password']

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    async def on_model_change(self, data, model, is_created, request) -> None:
        password = data.pop('password', None)
        if password:
            model.hashed_password = AuthUtils().get_password_hash(password)


class DropAdmin(ModelView, model=Drop):
    column_list = [Drop.id, Drop.title, Drop.artist_id, Drop.genre_id, Drop.is_deleted, Drop.is_archived]
    column_searchable_list = [Drop.title]
    column_sortable_list = [Drop.title]
    column_default_sort = [(Drop.title, True)]
    column_filterable_list = [Drop.is_archived]

class GenreAdmin(ModelView, model=Genre):
    column_list = [Genre.id, Genre.name, Genre.slug]
