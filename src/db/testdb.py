import logging

import sqlcipher3
from sqlalchemy import create_engine, event

from src.data.Base import Base

# Убедитесь, что ключ правильный
DATABASE_KEY = "564236"
uri_db = "/home/chris/PycharmProjects/Projects/LearnEnglishSubtitles/res/db/myTestDB.db"
DATABASE_URL = f"sqlite:///{uri_db}"

# Включаем логирование для отслеживания ошибок
logging.basicConfig(level=logging.DEBUG)

# Создаем подключение через SQLAlchemy с использованием SQLCipher
engine = create_engine(DATABASE_URL, module=sqlcipher3, echo=True)


# Установка ключа для SQLCipher
@event.listens_for(engine, "connect")
def set_sqlcipher_key(dbapi_connection, connection_record):
    logging.debug("Setting SQLCipher key...")
    cursor = dbapi_connection.cursor()
    cursor.execute(f"PRAGMA key = '{DATABASE_KEY}';")
    cursor.execute("PRAGMA cipher_version;")  # Проверяем версию SQLCipher
    cursor.execute("PRAGMA foreign_keys=ON")  # Включаем поддержку внешних ключей
    cursor.close()


# Функция инициализации базы данных
def init_db():
    logging.debug("Initializing database...")
    Base.metadata.create_all(bind=engine)


# Если это основной скрипт, запускаем
if __name__ == "__main__":
    init_db()
