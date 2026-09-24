import os


class Config:
    SECRET_KEY = "clave-secreta-desarrollo"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(
        os.path.join("instance", "tienda.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = True