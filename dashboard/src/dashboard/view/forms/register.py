from wtforms import validators, form, fields

from dashboard.entities.user import User
from dashboard.repository.sqlite import get_sql_connection


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if get_sql_connection().session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')
