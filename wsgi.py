import sqlite3
from flask import g
from flask import Flask
application = Flask(__name__)

DATABASE=/etc/freshcase/ecs.db

@application.route("/")
def hello():
    return "Hello World and flask"

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
if __name__ == "__main__":
    application.run()
