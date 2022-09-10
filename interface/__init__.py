"""Initialize Flask app."""
from flask_assets import Environment
from config import MyFlask

url = 'http://127.0.0.1:5000/api'

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = MyFlask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from api import routes
        from logic import routes
        from interface import routes

        from .views.dashboard import init_dashboard
        from .views.assets import compile_static_assets

        compile_static_assets(assets)
        app = init_dashboard(app)
        return app
