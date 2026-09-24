import json
import os

import click
from flask import current_app

from .extensions import db
from .models import Categoria, Producto


@click.command("init-db")
def init_db():
    """Crea las tablas de la base de datos."""
    db.create_all()

    click.echo("Base de datos inicializada correctamente.")


@click.command("reset-db")
def reset_db():
    """Borra todas las tablas y las vuelve a crear."""
    db.drop_all()
    db.create_all()

    click.echo("Base de datos reiniciada correctamente.")


@click.command("seed-db")
def seed_db():
    """Carga los productos desde productos.json."""
    
    ruta = os.path.join(
        current_app.root_path,
        "data",
        "productos.json"
    )

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            productos = json.load(archivo)

        for datos in productos:

            # Buscar si el producto ya existe
            producto_existente = Producto.query.filter_by(
                sku=datos["sku"]
            ).first()

            if producto_existente:
                click.echo(
                    f"SKU {datos['sku']} ya existe. Se omite."
                )
                continue

            # Buscar la categoría
            categoria = Categoria.query.filter_by(
                nombre=datos["categoria"]
            ).first()

            # Si no existe, crearla
            if categoria is None:
                categoria = Categoria(
                    nombre=datos["categoria"]
                )

                db.session.add(categoria)

                # Envía el INSERT para obtener el ID
                db.session.flush()

            # Crear el producto
            producto = Producto(
                sku=datos["sku"],
                marca=datos["marca"],
                nombre=datos["nombre"],
                precio=datos["precio"],
                foto=datos.get("foto"),
                stock=datos.get("stock", 0),
                activo=datos.get("activo", True),
                categoria_id=categoria.id
            )

            db.session.add(producto)

        # Guardar todo de una sola vez
        db.session.commit()

        click.echo("Productos cargados correctamente.")

    except Exception as error:
        db.session.rollback()

        click.echo(
            f"Error al cargar los productos: {error}"
        )