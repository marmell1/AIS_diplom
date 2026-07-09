from models import Products, Warehouses, WarehousesLoading, StockMovement
from database import get_session
from datetime import datetime
from sqlalchemy import select
from _3_Prepare import wh_l_expansion as wh_l_expansion


def main():
    pass


def handler(di: dict[str, str | int])->None:  # берем входящий dict
    today = datetime.now()
    with get_session() as session:
        #проверить что склад не переполнен

        #перемещение со склада либо от поставщика
        stmt = select(Warehouses).where(Warehouses.id == di["wh_out"])
        whl1 = session.scalars(stmt).one_or_none()

        stmt = select(WarehousesLoading).where(WarehousesLoading.warehouse_id == di["wh_out"],
                                               WarehousesLoading.product_id == di["product_id"])
        whl2 = session.scalars(stmt).one_or_none()

        if whl2 and whl2.quantity < di["count"]:
            raise ValueError("На указанном складе недостаточно данного товара для перемещения")


        if whl1: change_wh(session, di["wh_out"], di["product_id"], (-1 * di["count"]))

        # внесение в реестр
        add_stock_movement(session, di["input_type"], di["resp"], di["wh_in"], di["wh_out"], di["product_id"],
                           di["count"], di["date"] if "date" in di.keys() else today.date())

        # перемещение на склад либо к подрядчику
        stmt = select(Warehouses).where(Warehouses.id == di["wh_in"])
        whl1 = session.scalars(stmt).one_or_none()
        if whl1: change_wh(session, di["wh_in"], di["product_id"], (di["count"]))


def change_wh(session, wh: int | str, product_id: int, count: int)->None:
    print("изменяем количество товара на складе")

    stmt = select(WarehousesLoading).where(WarehousesLoading.warehouse_id == wh,
                                           WarehousesLoading.product_id == product_id)
    whl1 = session.scalars(stmt).one_or_none()

    if not whl1:
        whl_ = WarehousesLoading(warehouse_id=wh, warehouse_name="", product_id=product_id, product_name="", quantity=0,
                                 capacity=0)
        session.add(whl_)
        session.commit()

        wh_l_expansion()
        whl1 = session.scalars(stmt).one_or_none()

    whl1.quantity += count
    session.commit()
    session.refresh(whl1)

    # изменяем количество товара на складе
    # плюс проверки по неотрицательным значениям, по наличию такой строки в таблице


def add_stock_movement(session, input_type:str, resp:str, wh_in:str, wh_out:str, product_id:int, count:int, date:str)->None:
    print("внесение записи в реестр")

    sm1 = StockMovement(input_type=input_type, input_type_resp=resp, source=wh_out, destination=wh_in,
                        product_id=product_id, product_quantity=count, shipment_date=date)
    session.add(sm1)
    session.commit()
    print("добавили строку в реестр операций")


if __name__ == "__main__":
    main()
