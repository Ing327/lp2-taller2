# Taller 2 - Tienda Virtual

# AUTOR

Gustavo Adolfo Valencia Agudelo


## Descripción

Este proyecto corresponde al Taller 2 de programación y consiste en el desarrollo de una tienda virtual utilizando Flask, SQLite y SQLAlchemy.

La aplicación permite visualizar un catálogo de productos, consultar información detallada de cada producto, buscar productos mediante su SKU y filtrar los productos por categoría.

También se implementó el manejo de productos disponibles y agotados de acuerdo con su cantidad de stock.

## Tecnologías utilizadas

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS
- Ubuntu / WSL
- Git y GitHub

## Estructura del proyecto

```text
lp2-taller2/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── commands.py
│   ├── routes.py
│   ├── data/
│   │   └── productos.json
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── detalle.html
│       └── categorias.html
├── instance/
│   └── tienda.db
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Funcionalidades

### Catálogo de productos

La página principal muestra los productos registrados en la base de datos.

Cada producto muestra:

- Imagen
- Nombre
- Marca
- SKU
- Precio
- Stock
- Categoría
- Estado del producto
- Botón para ver el detalle

### Búsqueda por SKU

Se puede buscar un producto utilizando su SKU.

Ejemplo:

```text
AUD-001
```

La ruta de búsqueda es:

```text
/buscar?sku=AUD-001
```

La búsqueda redirige al detalle del producto correspondiente.

### Detalle de producto

Cada producto tiene una página individual utilizando su SKU.

Ruta:

```text
/producto/<sku>
```

Ejemplo:

```text
/producto/AUD-001
```

La página muestra:

- Imagen
- Nombre
- Marca
- SKU
- Categoría
- Precio
- Stock
- Estado del producto

### SKU inexistente

Cuando se consulta un SKU que no existe, la aplicación responde con HTTP 404.

Ejemplo:

```text
/producto/NO-EXISTE
```

Resultado esperado:

```text
404 Not Found
```

Esto se implementa utilizando:

```python
.first_or_404()
```

### Filtro por categoría

El catálogo permite filtrar los productos según su categoría.

Ejemplos:

```text
Todas las categorías
Audio
Periféricos
Monitores
Celulares
```

### Página de categorías

La aplicación cuenta con una página independiente para consultar las categorías.

Ruta:

```text
/categorias
```

En esta página se muestran las categorías registradas y la cantidad de productos asociados.

### Estado del producto

Los productos cuentan con información de stock y estado.

Un producto se considera disponible cuando:

```text
activo = True
```

y:

```text
stock > 0
```

Cuando no cumple estas condiciones se muestra como:

```text
Agotado
```

## Modelo de datos

El proyecto utiliza dos entidades principales.

### Categoria

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Identificador de la categoría |
| nombre | String | Nombre de la categoría |

El nombre de la categoría es único.

### Producto

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Identificador del producto |
| sku | String | Código único del producto |
| marca | String | Marca del producto |
| nombre | String | Nombre del producto |
| precio | Float | Precio del producto |
| foto | String | Ruta de la imagen |
| stock | Integer | Cantidad disponible |
| activo | Boolean | Estado activo del producto |
| categoria_id | Integer | Categoría relacionada |

La relación permite que varios productos pertenezcan a una misma categoría.

## Base de datos

La aplicación utiliza SQLite.

La base de datos se encuentra en:

```text
instance/tienda.db
```

SQLAlchemy se utiliza para realizar las operaciones sobre la base de datos mediante modelos.

## Comandos de Flask

### Inicializar la base de datos

```bash
flask init-db
```

### Reiniciar la base de datos

```bash
flask reset-db
```

### Cargar productos y categorías

```bash
flask seed-db
```

Los datos se cargan desde:

```text
app/data/productos.json
```

## Instalación

### 1. Entrar al proyecto

```bash
cd ~/taller2/lp2-taller2
```

### 2. Crear el entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Inicializar la base de datos

```bash
flask init-db
```

### 6. Cargar los datos

```bash
flask seed-db
```

## Ejecución

Para iniciar la aplicación:

```bash
python3 run.py
```

La aplicación estará disponible normalmente en:

```text
http://127.0.0.1:5000
```

## Rutas principales

| Ruta | Función |
|---|---|
| `/` | Catálogo de productos |
| `/buscar?sku=AUD-001` | Buscar producto por SKU |
| `/producto/<sku>` | Mostrar detalle de un producto |
| `/categorias` | Mostrar categorías |

## Ejemplos de uso

### Página principal

```text
http://127.0.0.1:5000/
```

### Buscar un producto

```text
http://127.0.0.1:5000/buscar?sku=AUD-001
```

### Ver detalle

```text
http://127.0.0.1:5000/producto/AUD-001
```

### Probar SKU inexistente

```text
http://127.0.0.1:5000/producto/NO-EXISTE
```

Resultado esperado:

```text
404 Not Found
```

### Ver categorías

```text
http://127.0.0.1:5000/categorias
```

## Imágenes

Las imágenes de los productos se almacenan en:

```text
app/static/images/
```

Las rutas de las imágenes se registran en `productos.json`.

Ejemplo:

```json
{
    "sku": "AUD-001",
    "marca": "Sony",
    "nombre": "Audífonos WH-1000XM4",
    "precio": 1199000,
    "foto": "images/audifonos-sony.jpg"
}
```

## Diseño

La aplicación utiliza CSS para proporcionar:

- Encabezado centrado
- Nombre de la tienda destacado
- Tarjetas de productos
- Botones
- Filtro por categorías
- Búsqueda por SKU
- Página de detalle
- Estados de disponible y agotado
- Diseño adaptable para diferentes tamaños de pantalla

## Pruebas principales

### Producto existente

Ingresar un SKU válido:

```text
AUD-001
```

Debe mostrar el detalle del producto.

### Producto inexistente

Ingresar:

```text
NO-EXISTE
```

Debe responder:

```text
404 Not Found
```

### Filtro por categoría

Seleccionar una categoría y comprobar que solamente se muestran los productos pertenecientes a ella.

### Productos agotados

Comprobar que un producto con:

```text
stock = 0
```

aparece como:

```text
Agotado
```

## Autor

Proyecto desarrollado como parte del Taller 2 de programación.
