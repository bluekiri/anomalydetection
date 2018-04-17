from flask import url_for, request
from flask_admin import expose, AdminIndexView
from flask_admin.helpers import validate_form_on_submit
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from dashboard.entities.user import User
from dashboard.repository.sqlite import get_sql_connection
from dashboard.view.forms.login import LoginForm
from dashboard.view.forms.register import RegistrationForm


class LoginAdminView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(LoginAdminView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated():
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(LoginAdminView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db = get_sql_connection()
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(LoginAdminView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))
