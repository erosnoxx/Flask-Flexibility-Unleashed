from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_pydantic_spec import FlaskPydanticSpec

db = SQLAlchemy()
lm = LoginManager()
spec = FlaskPydanticSpec('flask', title='Maps')

def init_app(app):
    db.init_app(app)
    lm.init_app(app)
    Migrate(app, db)
    spec.register(app)