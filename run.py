from app import create_app
from app.extensions import db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import Producto, Categoria

    return {
        "db": db,
        "Producto": Producto,
        "Categoria": Categoria
    }


if __name__ == "__main__":
    app.run(debug=True)