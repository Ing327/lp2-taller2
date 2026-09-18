"""
Application factory de la Tienda Virtual (versión con base de datos).

Respecto al Taller 1, create_app() ahora también:
  - carga la configuración desde config.py
  - inicializa la extensión SQLAlchemy
  - registra los comandos de terminal (flask init-db / flask seed-db)
"""

import os

from flask import Flask

from config import Config
from .extensions import db


def create_app(config_class=Config):
    """Crea y configura la instancia de la aplicación Flask."""
    app = Flask(__name__)

    # TODO 1: Carga la configuración de la clase recibida.
    #         Pista: app.config.from_object(config_class)

    # Asegura que exista la carpeta instance/ donde vivirá el archivo .db
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    # TODO 2: Inicializa SQLAlchemy con esta aplicación.
    #         Pista: db.init_app(app)

    # Importar los modelos DENTRO de la factory (y después de init_app)
    # garantiza que SQLAlchemy conozca las tablas al crear la base de datos.
    from . import models  # noqa: F401

    # TODO 3: Importa el blueprint 'main' desde .routes y regístralo
    #         con app.register_blueprint(main)

    # Registra los comandos personalizados de terminal.
    from .commands import registrar_comandos

    registrar_comandos(app)

    return app
