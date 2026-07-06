
import models
from database import init_db

def main():
    # Создаем таблицы в БД
    print("Создание таблиц...")
    init_db()
    print("✓ Таблицы созданы\n")

if __name__ == "__main__":
    main()