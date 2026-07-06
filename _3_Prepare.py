from models import Products, Warehouses, WarehousesLoading
from database import get_session
from sqlalchemy import select

from sqlalchemy import ForeignKey, String, update, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def main():
    # print("expansion")
    wh_l_expansion()


def wh_l_expansion(): #Добавление расшифровки столбцов загрузки склада
    with get_session() as session:
        print("Добавление расшифровки столбцов загрузки склада")
        # 1. Создаем подзапрос. scalar_subquery() преобразует его в одиночное значение.
        subquery = (
            select(Warehouses.name)
            .where(Warehouses.id == WarehousesLoading.warehouse_id)
            .scalar_subquery()
        )
        subquery2 = (
            select(Products.name)
            .where(Products.id == WarehousesLoading.product_id)
            .scalar_subquery()
        )

        # 2. Формируем инструкцию UPDATE
        # Значение столбца будет заменяться результатом выполнения subquery
        stmt = update(WarehousesLoading).values(warehouse_name=subquery)
        stmt2 = update(WarehousesLoading).values(product_name=subquery2)

        # 3. Выполняем одной транзакцией на стороне SQLite
        session.execute(stmt)
        session.execute(stmt2)
        session.commit()
        #session.refresh(WarehousesLoading)


'''
заполнить empty_space  в загрузке складов
проверить партии и остатки на складах на просрочку
проверить остатки на складах на соответствие температурному режиму
проверить что все объемы на складах не больше вместимости склада
заполнить capacity в loading

проверка иконвертация форматов при вводе cli


'''

if __name__ == "__main__":
    main()
