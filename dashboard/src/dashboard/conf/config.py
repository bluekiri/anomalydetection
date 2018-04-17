import os

# Flask configuration
SECRET_KEY = '123456790'
DATA_DB_FILE = os.environ["DATA_DB_FILE"]
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATA_DB_FILE
SQLALCHEMY_ECHO = True
