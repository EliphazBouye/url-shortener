from flask import Flask
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
config = dotenv_values(".env")

db = SQLAlchemy()
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config['DB_USER']}:{config['DB_PASS']}@localhost/{config['DB_NAME']}"
# initialize the app with the extension
db.init_app(app)
