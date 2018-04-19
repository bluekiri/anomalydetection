from flask import Flask, url_for, redirect, render_template, request

# Create Flask application
from flask_admin import Admin
from flask_login import LoginManager

from anomalydetection.dashboard.conf.config import SECRET_KEY, DATA_DB_FILE, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO
from anomalydetection.dashboard.interactor.get_prediction_signal import GetPredictionSignal
from anomalydetection.dashboard.repository.predictions_signal_repository import PredictionSignalRepository
from anomalydetection.dashboard.repository.sqlite import get_sql_connection
import os
current_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = SECRET_KEY
app.config['STATIC_FOLDER'] = current_path +'/static'
# Create in-memory database
app.config['DATABASE_FILE'] = DATA_DB_FILE
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
get_sql_connection(app)

from anomalydetection.dashboard.entities.user import User
from anomalydetection.dashboard.interactor.is_current_user_validate import IsCurrentUserValidate
from anomalydetection.dashboard.view.home_view import HomeView
from anomalydetection.dashboard.view.login_admin_view import LoginAdminView


# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return get_sql_connection().session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home.index'))
    return render_template('login.html', error=error)


init_login()

admin = Admin(app, 'Example: Auth', index_view=LoginAdminView(), base_template='my_master.html')

is_current_user_validate = IsCurrentUserValidate()

predictions_signal_repository = PredictionSignalRepository()

get_prediction_signal = GetPredictionSignal(predictions_signal_repository)

admin.add_view(
    HomeView(User, get_sql_connection().session, is_current_user_validate, endpoint="home",
             get_prediction_signal=get_prediction_signal))

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
