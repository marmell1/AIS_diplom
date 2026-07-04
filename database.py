"""Конфигурация и подключение к БД SQLite."""

from typing import Generator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager

# Путь к файлу БД в корне проекта
DATABASE_URL = "sqlite:///app.db"

# Создание engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Вывод SQL запросов при разработке
)

# Фабрика сессий
SessionLocal = sessionmaker(
   bind=engine,
   autoflush=False,
   expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()


@contextmanager
def get_session()-> Generator[Session, Any, None]:
    """Контекстный менеджер для сессии БД.

    Используйте как:
        with get_session() as session:
            ...

    Менеджер гарантирует закрытие сессии и делает rollback при исключении.
    Коммиты должны выполняться вручную (session.commit()), если это требуется.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    # metadata.create_all проверяет существование таблиц и создает отсутствующие
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Удалить все таблицы из БД."""
    Base.metadata.drop_all(bind=engine)

