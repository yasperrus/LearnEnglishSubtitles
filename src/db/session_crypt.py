import sqlcipher3
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

import src.data  # noqa: F401
from src.data.Base import Base

load_dotenv()
# DATABASE_KEY = os.getenv("DATABASE_KEY")
DATABASE_KEY = "564236"
if not DATABASE_KEY:
    raise RuntimeError(
        "DATABASE_KEY не найден. Установите переменную окружения или .env файл"
    )

uri_db = "/home/chris/PycharmProjects/Projects/LearnEnglishSubtitles/res/db/myTestDB.db"
# uri_db = os.path.join(base_path(), "res", "db", "myTestDB.db")
print(uri_db)
DATABASE_URL = f"sqlite:///{uri_db}"
engine = create_engine(DATABASE_URL, module=sqlcipher3, echo=False)


@event.listens_for(engine, "connect")
def set_sqlcipher_key(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute(f"PRAGMA key = '{DATABASE_KEY}';")
    cursor.execute("PRAGMA cipher_version;")
    # print("SQLCipher version:", cursor.fetchone())
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
