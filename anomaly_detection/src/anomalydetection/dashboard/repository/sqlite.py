from flask_sqlalchemy import SQLAlchemy

db = None


def get_sql_connection(app=None):
    global db
    if db is None and app is not None:
        db = SQLAlchemy(app)
    if db is None:
        raise Exception("You must to initialize the sql connection.")
    return db
