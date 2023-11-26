from app.blueprints.api.v1.post import api

def init_app(app):
    app.register_blueprint(api)