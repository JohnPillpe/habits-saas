"""Crea las tablas de la base de datos si no existen."""

from database import Base, engine
import models  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()
