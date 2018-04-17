from werkzeug.security import check_password_hash
from wtforms import form, fields, validators

from dashboard.entities.user import User
from dashboard.repository.sqlite import get_sql_connection


class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return get_sql_connection().session.query(User).filter_by(login=self.login.data).first()
