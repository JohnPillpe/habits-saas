from app.db.database import Base, engine
from app.models import models


def init_db() -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "DROP SCHEMA public CASCADE;"
        )
        connection.exec_driver_sql(
            "CREATE SCHEMA public;"
        )

    Base.metadata.create_all(bind=engine)

    print("Base de datos recreada completamente.")


if __name__ == "__main__":
    init_db()