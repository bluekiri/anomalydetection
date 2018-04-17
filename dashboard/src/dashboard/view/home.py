# Create customized model view class
from flask_admin.contrib import sqla


class MyModelView(sqla.ModelView):

    def __init__(self, model, session, login_auth):
        super().__init__(model, session)
        self.login_auth = login_auth

    def is_accessible(self):
        return self.login_auth.current_user.is_authenticated()
