"""
Extensiones de Flask.

La instancia de SQLAlchemy se crea en un archivo aparte para evitar
importaciones circulares: models.py necesita 'db', y __init__.py necesita
tanto 'db' como los modelos. Teniéndola aquí, ambos pueden importarla sin
depender el uno del otro.
"""

from flask_sqlalchemy import SQLAlchemy

# Instancia global del ORM. Todavía no está ligada a ninguna aplicación:
# eso ocurre en create_app() con db.init_app(app).
db = SQLAlchemy()
