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

        stmt = update(WarehousesLoading).values(warehouse_name=subquery)
        stmt2 = update(WarehousesLoading).values(product_name=subquery2)

        session.execute(stmt)
        session.execute(stmt2)
        session.commit()


'''
заполнить empty_space  в загрузке складов
проверить что все цены в продуктах положительные
проверить что площадь помещения на складах положительная
проверить партии и остатки на складах на просрочку
проверить остатки на складах на соответствие температурному режиму
проверить что все объемы на складах не больше вместимости склада
заполнить capacity в loading
проверить неотрицательные остатки

проверка и конвертация форматов при вводе cli


'''

if __name__ == "__main__":
    main()
