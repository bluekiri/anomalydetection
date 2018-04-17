import os

from bokeh.embed import components
from flask import Flask, url_for, redirect, render_template, request

# Create Flask application
from flask_admin import Admin
from flask_login import LoginManager

from dashboard.src.dashboard.repository.sqlite import get_sql_connection

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
get_sql_connection(app)

from dashboard.src.dashboard.initialize_db import build_sample_db
from dashboard.src.dashboard.entities.user import User
from dashboard.src.dashboard.interactor.is_current_user_validate import IsCurrentUserValidate
from dashboard.src.dashboard.view.home import MyModelView
from dashboard.src.dashboard.view.my_admin_index import MyAdminIndexView


# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return get_sql_connection().session.query(User).get(user_id)


# # Flask views
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


def create_figure():
    from bokeh.plotting import figure
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend="Temp.", line_width=2)
    # Set the y axis label
    return p


@app.route('/home')
def home():
    plot = create_figure()
    script, div = components(plot)
    return render_template("home.html", script=script, div=div)


init_login()

admin = Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html')

is_current_user_validate = IsCurrentUserValidate()

admin.add_view(MyModelView(User, get_sql_connection().session, is_current_user_validate))

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
