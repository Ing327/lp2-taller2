"""
Comandos personalizados de terminal (Flask CLI).

Permiten ejecutar tareas administrativas desde la terminal, por ejemplo:

    flask init-db     -> crea las tablas en la base de datos
    flask seed-db     -> carga los productos del JSON a la base de datos

Estos comandos se registran en create_app().
"""

import json
import os

import click

from .extensions import db
from .models import Categoria, Producto

RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), "data", "productos.json")


def registrar_comandos(app):
    """Asocia los comandos a la aplicación Flask recibida."""

    @app.cli.command("init-db")
    def init_db():
        """Crea todas las tablas definidas en models.py."""
        # TODO 1: Llama a db.create_all() para crear las tablas.
        # TODO 2: Muestra un mensaje de confirmación con click.echo(...)
        pass

    @app.cli.command("reset-db")
    def reset_db():
        """Borra y vuelve a crear todas las tablas (¡pierde los datos!)."""
        # TODO 3: Llama a db.drop_all() y luego a db.create_all()
        # TODO 4: Muestra un mensaje de confirmación
        pass

    @app.cli.command("seed-db")
    def seed_db():
        """Carga los productos de productos.json en la base de datos."""

        # --- Leer el archivo JSON -------------------------------------
        # TODO 5: Abre RUTA_PRODUCTOS con encoding="utf-8" y usa
        #         json.load() para obtener la lista de productos.
        # datos = ...

        # --- Insertar categorías y productos --------------------------
        # Por cada producto del JSON debes:
        #
        # TODO 6: Buscar si su categoría ya existe en la base de datos:
        #         categoria = Categoria.query.filter_by(
        #             nombre=item["categoria"]).first()
        #
        # TODO 7: Si no existe, crearla y agregarla a la sesión:
        #         categoria = Categoria(nombre=item["categoria"])
        #         db.session.add(categoria)
        #         db.session.flush()   # asigna el id sin confirmar aún
        #
        # TODO 8: Evitar duplicados: si ya existe un Producto con ese sku
        #         (Producto.query.filter_by(sku=item["sku"]).first()),
        #         saltarlo con 'continue'.
        #
        # TODO 9: Crear el objeto Producto con los datos del JSON y
        #         asignarle categoria_id=categoria.id, luego
        #         db.session.add(producto)

        # --- Confirmar la transacción ---------------------------------
        # TODO 10: Llama a db.session.commit() para guardar TODO de una
        #          vez. Hasta este momento nada se ha escrito en disco.

        # TODO 11: Muestra cuántos productos se cargaron con click.echo(...)
        pass
