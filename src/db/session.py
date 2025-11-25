from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.data  # noqa: F401
from config import resource_path
from src.data.Base import Base

# Загружаем переменные окружения из .env файла
load_dotenv()

# Устанавливаем путь к базе данных (обычная SQLite база)
uri_db = resource_path("res/db/myTestDBNoCrypt.db")
print(f"Connecting to database at: {uri_db}")

# Устанавливаем строку подключения к не зашифрованной базе данных
DATABASE_URL = f"sqlite:///{uri_db}"

# Создаем движок без использования SQLCipher (обычная SQLite)
engine = create_engine(DATABASE_URL, echo=False)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для инициализации базы данных (создание всех таблиц)
def init_db():
    Base.metadata.create_all(bind=engine)


# Если это основной скрипт, запускаем
if __name__ == "__main__":
    init_db()
