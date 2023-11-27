from app.blueprints.api.v1.post import post_api
from app.blueprints.api.v1.get import get_api


def init_app(app):
    app.register_blueprint(post_api)
    app.register_blueprint(get_api)
