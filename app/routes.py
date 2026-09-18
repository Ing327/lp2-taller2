"""
Rutas (vistas) de la Tienda Virtual.

CAMBIO CLAVE respecto al Taller 1:
ya NO leemos productos.json en cada petición. Ahora consultamos la base de
datos a través del ORM. Las funciones cargar_productos() y
buscar_producto_por_sku() desaparecen y se reemplazan por consultas
SQLAlchemy como Producto.query.all() o Producto.query.filter_by(...).
"""

from flask import Blueprint, render_template, abort, request

from .models import Producto, Categoria

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Página principal: catálogo de productos desde la base de datos.

    Soporta filtro opcional por categoría mediante query string:
        /?categoria=<id>
    """
    # Lee el parámetro ?categoria= de la URL (None si no viene).
    categoria_id = request.args.get("categoria", type=int)

    # TODO 1: Si categoria_id tiene valor, consulta solo los productos de
    #         esa categoría:
    #             productos = Producto.query.filter_by(
    #                 categoria_id=categoria_id).all()
    #         Si no viene, trae todos los productos:
    #             productos = Producto.query.all()

    # TODO 2: Consulta todas las categorías para pintar el menú de filtros:
    #         categorias = Categoria.query.order_by(Categoria.nombre).all()

    # TODO 3: Renderiza "index.html" enviando 'productos', 'categorias' y
    #         'categoria_id' (para marcar el filtro activo).
    pass


@main.route("/producto/<sku>")
def detalle(sku):
    """Detalle de un producto, buscado por su SKU en la base de datos."""

    # TODO 4: Busca el producto por SKU. La forma más limpia es:
    #             producto = Producto.query.filter_by(sku=sku).first_or_404()
    #         first_or_404() devuelve el objeto o lanza un 404 automáticamente,
    #         así te ahorras el 'if producto is None: abort(404)'.

    # TODO 5: Renderiza "detalle.html" pasándole el producto.
    pass


@main.route("/categorias")
def categorias():
    """Lista de categorías con la cantidad de productos de cada una."""

    # TODO 6: Consulta todas las categorías ordenadas por nombre.
    #         Gracias al backref definido en el modelo, dentro del template
    #         puedes usar categoria.productos para contar sus productos
    #         con el filtro |length de Jinja2.

    # TODO 7: Renderiza "categorias.html" con la lista obtenida.
    pass
