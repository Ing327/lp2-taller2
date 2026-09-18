# Taller 2 — Tienda Virtual con Flask, SQLite y SQLAlchemy

## Objetivo

Evolucionar la tienda virtual del **Taller 1** (que leía los productos desde un archivo JSON) hacia una aplicación con **base de datos SQLite**, administrada mediante el ORM **SQLAlchemy** a través de la extensión **Flask-SQLAlchemy**.

El archivo `productos.json` no desaparece: pasa a ser la **semilla** (seed) con la que poblamos la base de datos por primera vez. Al terminar sabrás:

- Qué es un ORM y por qué se prefiere sobre escribir SQL a mano.
- Definir modelos (tablas) como clases de Python.
- Crear relaciones entre tablas (uno-a-muchos) con llaves foráneas.
- Consultar, filtrar y ordenar datos con la API de consultas de SQLAlchemy.
- Crear comandos de terminal propios con el CLI de Flask.

## Requisitos previos

- Haber completado el **lp2-taller1**.
- Ubuntu / WSL2 con Python 3.10+.
- Conocimientos básicos de bases de datos relacionales (tabla, fila, columna, llave primaria, llave foránea).

> todos los comandos de esta guía se ejecutan dentro de tu distribución de Linux Ubuntu.
> Windows. Abre tu terminal de Ubuntu/WSL2 antes de continuar.

---

## ¿Por qué un ORM?

Sin ORM, para traer un producto tendrías que escribir SQL, ejecutarlo y convertir manualmente cada fila a un objeto de Python:

```python
cursor.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
fila = cursor.fetchone()   # una tupla: ('TEC-001', 'Logitech', ...)
```

Con un **ORM** (Object-Relational Mapper) trabajas con objetos Python y la librería genera el SQL por ti:

```python
producto = Producto.query.filter_by(sku=sku).first()
print(producto.nombre)     # acceso por atributo, no por índice
```

Ventajas: menos código repetitivo, menos errores de tipeo en SQL, protección automática contra inyección SQL, y portabilidad (el mismo código funciona con SQLite, PostgreSQL o MySQL cambiando solo la URI de conexión).

---

## Lista de tareas del taller

Esta es la hoja de ruta que seguiremos (ligeramente ampliada respecto al plan original, agregando pasos que son buena práctica y que necesitarás para poder ejecutar y probar tu proyecto):

---

## Paso 1 — Proyecto

Primero, realiza un **fork** del repositorio de **lp2-taller2** en tu cuenta GitHub, y luego **clona** tu copia del repositorio en tu espacio de trabajo.

---

## Paso 2 — Entorno virtual e instalación de SQLAlchemy

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy
```

`Flask-SQLAlchemy` es una extensión que integra SQLAlchemy con Flask: se encarga de crear la sesión de base de datos, ligarla al ciclo de vida de cada petición y ofrecer la sintaxis `Modelo.query`.

Actualiza el archivo de dependencias:

```bash
pip freeze > requirements.txt
```

> **SQLite no se instala.** Viene incluido en la librería estándar de Python (módulo `sqlite3`) y la base de datos completa es un único archivo en disco. Por eso es ideal para aprender: cero configuración, cero servidor corriendo.

---

## Paso 3 — Estructura del proyecto

```
lp2-taller2/
├── app/
│   ├── __init__.py          # Factory: config + db + blueprints + comandos
│   ├── extensions.py        # instancia db = SQLAlchemy()
│   ├── models.py            # modelos Categoria y Producto
│   ├── commands.py          # comandos init-db / reset-db / seed-db
│   ├── routes.py            # con consultas la BD
│   ├── data/
│   │   └── productos.json   # semilla de datos para la BD
│   ├── static/
│   │   ├── css/style.css
│   │   └── images/
│   └── templates/
│       ├── base.html        # menú de navegación
│       ├── index.html       # filtros + objetos
│       ├── detalle.html     # stock y categoría
│       └── categorias.html  # listado de categorías
├── instance/
│   └── tienda.db            # archivo de base de datos SQLite
├── config.py                # configuración de la aplicación
├── requirements.txt
├── run.py
├── .gitignore
└── docs/GUIA.md
```

> **¿Por qué `instance/`?** Es una convención de Flask para archivos propios de *esta instalación*: la base de datos, claves secretas, etc. Nunca se suben al repositorio.

---

## Paso 4 — Configuración (`config.py`)

Archivo en la raíz del proyecto. Debe definir una clase `Config` con:

- `SECRET_KEY`: cadena para firmar sesiones.
- `SQLALCHEMY_DATABASE_URI`: la ruta de conexión. Para SQLite el formato es
  `sqlite:///` seguido de la **ruta absoluta** al archivo `.db`.
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`.
- `SQLALCHEMY_ECHO`: ponlo temporalmente en `True` para ver el SQL generado.

Revisa los `# TODO` del archivo `config.py` entregado.

---

## Paso 5 — Los modelos (`app/models.py`)

Un **modelo** es una clase Python que hereda de `db.Model` y representa una tabla. Cada `db.Column` es una columna.

### Modelo `Categoria`

| Campo  | Tipo         | Restricciones                 |
|--------|--------------|-------------------------------|
| id     | Integer      | primary_key                   |
| nombre | String(80)   | not null, unique              |

Además define la relación:

```python
productos = db.relationship("Producto", backref="categoria", lazy=True)
```

Esto crea dos caminos de navegación:
- `categoria.productos` → lista de productos de esa categoría.
- `producto.categoria` → el objeto categoría al que pertenece (esto lo genera automáticamente el `backref`).

### Modelo `Producto`

| Campo        | Tipo         | Restricciones                          |
|--------------|--------------|-----------------------------------------|
| id           | Integer      | primary_key                            |
| sku          | String(20)   | not null, unique                       |
| marca        | String(80)   | not null                               |
| nombre       | String(160)  | not null                               |
| precio       | Float        | not null                               |
| foto         | String(200)  | nullable                               |
| stock        | Integer      | not null, default 0                    |
| activo       | Boolean      | not null, default True                 |
| categoria_id | Integer      | ForeignKey("categorias.id"), not null  |

También implementarás:
- `__repr__()`: representación legible para depuración.
- Una propiedad `disponible` que retorne `True` si el producto está activo y tiene stock.

> **Nota importante:** el `sku` deja de ser el identificador interno; ahora la llave primaria es un `id` numérico autoincremental. El `sku` sigue siendo único y lo seguimos usando en las URLs por ser más legible.

Completa los `# TODO` de `app/models.py`.

---

## Paso 6 — Ampliar `productos.json`

Cada producto ahora incluye tres campos nuevos:

```json
{
  "sku": "AUD-001",
  "marca": "Sony",
  "nombre": "Audífonos WH-1000XM4",
  "precio": 1199000,
  "foto": "images/audifonos-sony.jpg",
  "stock": 0,
  "activo": true,
  "categoria": "Audio"
}
```

**Tu tarea:** agrega al menos 8 productos repartidos en 3 o más categorías distintas, e incluye deliberadamente alguno con `stock: 0` para poder probar el estado "Agotado".

---

## Paso 7 — Comandos de terminal (`app/commands.py`)

En vez de crear las tablas manualmente, definimos comandos propios que se ejecutan con el CLI de Flask:

| Comando           | Qué hace                                          |
|-------------------|---------------------------------------------------|
| `flask init-db`   | Crea las tablas con `db.create_all()`             |
| `flask reset-db`  | `drop_all()` + `create_all()` (borra todo)        |
| `flask seed-db`   | Lee `productos.json` e inserta los registros      |

La lógica de `seed-db` que debes implementar:

1. Leer el JSON.
2. Por cada producto, buscar su categoría; si no existe, crearla.
3. Saltar los productos cuyo SKU ya esté en la base (evitar duplicados).
4. Crear el objeto `Producto` y agregarlo a la sesión.
5. Un único `db.session.commit()` al final.

> **Concepto clave — la sesión:** `db.session.add()` no escribe en la base de datos, solo marca el objeto como pendiente. Nada se guarda hasta `db.session.commit()`. Si algo falla en el medio, puedes revertir todo con `db.session.rollback()`. A esto se le llama **transacción**.
>
> `db.session.flush()` es un punto intermedio: envía los INSERT a la base (por eso el objeto ya obtiene su `id`) pero sin confirmar la transacción. Lo necesitamos para poder usar `categoria.id` en el producto antes del commit final.

Completa los `# TODO` de `app/commands.py`.

---

## Paso 8 — Rutas con consultas ORM (`app/routes.py`)

Las funciones `cargar_productos()` y `buscar_producto_por_sku()` del Taller 1 **se eliminan**. Ahora las reemplazan consultas del ORM.

Equivalencias de referencia:

| Necesitas                        | Consulta SQLAlchemy                                      |
|----------------------------------|----------------------------------------------------------|
| Todos los productos              | `Producto.query.all()`                                   |
| Uno por SKU                      | `Producto.query.filter_by(sku=sku).first()`              |
| Uno por SKU, o error 404         | `Producto.query.filter_by(sku=sku).first_or_404()`       |
| Por llave primaria               | `Producto.query.get(1)`                                  |
| Filtrar por categoría            | `Producto.query.filter_by(categoria_id=3).all()`         |
| Ordenar                          | `Producto.query.order_by(Producto.precio).all()`         |
| Comparaciones                    | `Producto.query.filter(Producto.precio > 100000).all()`  |
| Contar                           | `Producto.query.count()`                                 |

Rutas a implementar:

- `/` → catálogo, con filtro opcional `?categoria=<id>` leído con
  `request.args.get("categoria", type=int)`.
- `/producto/<sku>` → detalle usando `first_or_404()`.
- `/categorias` → listado de categorías (vista nueva).

Completa los `# TODO` de `app/routes.py`.

---

## Paso 9 — Plantillas

El cambio más importante: **los productos ya no son diccionarios, son objetos**. En Jinja2 la sintaxis con punto (`producto.nombre`) funciona en ambos casos, así que el HTML del Taller 1 sigue sirviendo, pero ahora puedes aprovechar cosas nuevas:

- `producto.categoria.nombre` → navega la relación hasta la otra tabla.
- `producto.disponible` → la propiedad que definiste en el modelo.
- `categoria.productos|length` → cuenta los productos de una categoría.

Archivos a completar: `index.html` (filtros + estado de stock), `detalle.html` (categoría y stock) y `categorias.html` (nuevo).

---

## Paso 10 — Ejecutar y probar

Con el entorno virtual activo, indica a Flask cuál es tu aplicación:

```bash
export FLASK_APP=run.py
```

> Para no repetirlo en cada terminal, puedes crear un archivo `.flaskenv` (requiere `pip install python-dotenv`) con la línea `FLASK_APP=run.py`.

Crea las tablas y carga los datos:

```bash
flask init-db
flask seed-db
```

Verifica que el archivo `instance/tienda.db` se haya creado:

```bash
ls -lh instance/
```

Explora los datos sin abrir el navegador, usando el shell interactivo:

```bash
flask shell
```

```python
>>> Producto.query.count()
>>> Producto.query.first()
>>> Categoria.query.all()
>>> p = Producto.query.filter_by(sku="TEC-001").first()
>>> p.categoria.nombre
>>> p.disponible
```

Finalmente, levanta el servidor:

```bash
python run.py
```

Y prueba en el navegador:

1. `/` — el catálogo completo.
2. `/?categoria=1` — catálogo filtrado.
3. `/producto/TEC-001` — el detalle, mostrando categoría y stock.
4. `/producto/NO-EXISTE` — debe dar 404.
5. `/categorias` — listado con el conteo por categoría.

### Inspeccionar la base de datos (opcional)

```bash
sudo apt install sqlite3      # si no lo tienes
sqlite3 instance/tienda.db
```

```sql
.tables
.schema productos
SELECT sku, nombre, stock FROM productos;
.quit
```

Compara ese SQL con las consultas ORM que escribiste: es exactamente lo que SQLAlchemy está generando por ti.

---

## Errores frecuentes

| Error | Causa probable |
|-------|----------------|
| `no such table: productos` | No ejecutaste `flask init-db`, o lo hiciste antes de definir los modelos. |
| `Could not locate a Flask application` | Falta `export FLASK_APP=run.py`. |
| `NOT NULL constraint failed` | Un campo obligatorio llegó vacío desde el JSON. |
| `UNIQUE constraint failed: productos.sku` | Intentaste insertar un SKU repetido (revisa el TODO de evitar duplicados). |
| Los cambios al modelo no se reflejan | `create_all()` NO modifica tablas existentes. Usa `flask reset-db` (o migraciones, ver extensiones). |
| `ImportError: cannot import name 'db'` | Importación circular: `db` debe vivir en `extensions.py`. |

---

## Checklist final

- [ ] `flask-sqlalchemy` instalado y `requirements.txt` actualizado.
- [ ] `config.py` apunta correctamente a `instance/tienda.db`.
- [ ] Modelos `Categoria` y `Producto` definidos con sus restricciones.
- [ ] Relación uno-a-muchos funcionando (`producto.categoria` y `categoria.productos`).
- [ ] `flask init-db` crea el archivo de base de datos.
- [ ] `flask seed-db` carga los productos sin duplicarlos al ejecutarlo dos veces.
- [ ] `/` muestra el catálogo desde la base de datos.
- [ ] El filtro por categoría funciona.
- [ ] `/producto/<sku>` muestra detalle y responde 404 con SKU inválido.
- [ ] `/categorias` muestra el conteo correcto por categoría.
- [ ] `instance/` y `*.db` están en `.gitignore`.

