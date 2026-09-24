from flask import Flask

from config import Config
from .extensions import db
from .routes import main
from .commands import init_db, reset_db, seed_db


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(main)

    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(seed_db)

    return app