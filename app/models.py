"""
Modelos de datos (ORM SQLAlchemy).

Cada clase que hereda de db.Model representa una TABLA de la base de datos,
y cada atributo db.Column representa una COLUMNA. SQLAlchemy se encarga de
traducir estas clases a SQL y de convertir las filas en objetos Python.
"""

from .extensions import db


class Categoria(db.Model):
    """Categoría a la que pertenece un producto (Periféricos, Audio, etc.)."""

    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)

    # TODO 1: Define la columna 'nombre':
    #         - Tipo db.String(80)
    #         - No puede ser nula (nullable=False)
    #         - Debe ser única (unique=True), no queremos categorías repetidas
    # nombre = db.Column(...)

    # Relación uno-a-muchos: una categoría tiene muchos productos.
    # 'backref' crea automáticamente el atributo producto.categoria
    # para poder navegar en sentido contrario.
    productos = db.relationship("Producto", backref="categoria", lazy=True)

    def __repr__(self):
        """Representación legible del objeto (útil al depurar)."""
        # TODO 2: Retorna algo como f"<Categoria {self.nombre}>"
        pass


class Producto(db.Model):
    """Producto del catálogo de la tienda."""

    __tablename__ = "productos"

    # Clave primaria autoincremental. Nota que ahora el SKU deja de ser
    # el identificador interno: la base de datos usa un id numérico.
    id = db.Column(db.Integer, primary_key=True)

    # TODO 3: Define las siguientes columnas con sus restricciones:
    #   sku      -> db.String(20),  unique=True, nullable=False
    #   marca    -> db.String(80),  nullable=False
    #   nombre   -> db.String(160), nullable=False
    #   precio   -> db.Float,       nullable=False
    #   foto     -> db.String(200), nullable=True  (puede no tener imagen)
    #   stock    -> db.Integer,     nullable=False, default=0
    #   activo   -> db.Boolean,     nullable=False, default=True
    #
    # sku = db.Column(...)
    # marca = db.Column(...)
    # ...

    # TODO 4: Define la llave foránea hacia la tabla 'categorias'.
    #         Pista: db.Column(db.Integer, db.ForeignKey("categorias.id"),
    #                          nullable=False)
    # categoria_id = db.Column(...)

    def __repr__(self):
        # TODO 5: Retorna algo como f"<Producto {self.sku} - {self.nombre}>"
        pass

    @property
    def disponible(self):
        """True si el producto está activo y tiene unidades en stock.

        TODO 6: Retorna True solamente si self.activo es verdadero
                Y self.stock es mayor que 0.
        """
        pass
