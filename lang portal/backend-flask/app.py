from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import *
from routes.words import words_bp
from routes.study_sessions import study_sessions_bp
from routes.study_activities import study_activities_bp
from routes.dashboard import dashboard_bp
from routes.groups import groups_bp

app.register_blueprint(words_bp)
app.register_blueprint(study_sessions_bp)
app.register_blueprint(study_activities_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(groups_bp)

if __name__ == '__main__':
    app.run(debug=True)