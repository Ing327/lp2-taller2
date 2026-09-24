from flask import Blueprint, render_template, request, redirect, url_for
from .models import Producto, Categoria

main = Blueprint("main", __name__)


@main.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)

    if categoria_id:
        productos = Producto.query.filter_by(
            categoria_id=categoria_id
        ).all()
    else:
        productos = Producto.query.all()

    categorias = Categoria.query.order_by(
        Categoria.nombre
    ).all()

    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias,
        categoria_seleccionada=categoria_id
    )


@main.route("/buscar")
def buscar():
    sku = request.args.get("sku", "").strip()

    if not sku:
        return redirect(url_for("main.index"))

    return redirect(url_for("main.detalle", sku=sku))


@main.route("/producto/<sku>")
def detalle(sku):
    producto = Producto.query.filter_by(
        sku=sku
    ).first_or_404()

    return render_template(
        "detalle.html",
        producto=producto
    )


@main.route("/categorias")
def categorias():
    categorias = Categoria.query.order_by(
        Categoria.nombre
    ).all()

    return render_template(
        "categorias.html",
        categorias=categorias
    )