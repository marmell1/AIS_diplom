from models import Products,Warehouses,WarehousesLoading,StockMovement
from database import get_session
from datetime import datetime
from sqlalchemy import select
from _3_Prepare import wh_l_expansion as wh_l_expansion

def main():
    # dict_input = get_input("CLI") # читаем источник
    # dict_input = {"wh_in":2,"wh_out":1,"product_id":3,"count":10}
    # print("test dict")
    # handler(dict_input)
    pass




def handler(di): # берем входящий dict
    today = datetime.now()
    with get_session() as session:
    #проверить что количество положительное
    #проверить что со склада не уйдет в минус штуки
    #проверить что склад не переполнен
        """
        исключения и ошибки - словарь
        input type левый
        ответсвенный не назван
        количество отрицательное или вообще строка
        дата не дата
        """
        add_stock_movement(session, di["input_type"], di["resp"], di["wh_in"], di["wh_out"], di["product_id"],
                           di["count"],di["date"] if "date" in di.keys() else today.date())

        stmt = select(Warehouses).where(Warehouses.id == di["wh_in"])
        whl1 = session.scalars(stmt).one_or_none()
        if whl1: change_wh(session, di["wh_in"], di["product_id"], (di["count"]))

        stmt = select(Warehouses).where(Warehouses.id == di["wh_out"])
        whl1 = session.scalars(stmt).one_or_none()
        if whl1: change_wh(session, di["wh_out"], di["product_id"], (-1*di["count"]))


def change_wh(session, wh:int|str, product_id:int, count:int):
    print ("изменяем количество товара на складе")

    """
    исключения и ошибки
    количество - строка или дробь
    
    """
    stmt = select(WarehousesLoading).where(WarehousesLoading.warehouse_id == wh, WarehousesLoading.product_id == product_id)
    whl1 = session.scalars(stmt).one_or_none()

    if not whl1:
        whl_ = WarehousesLoading(warehouse_id=wh, warehouse_name="", product_id=product_id, product_name="", batch_id=2, quantity=0,
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

def add_stock_movement(session, input_type, resp, wh_in, wh_out, product_id,count,date):
    print("внесение записи в реестр")

    sm1 = StockMovement(input_type = input_type, input_type_resp = resp,source = wh_out,destination = wh_in,
                        product_id = product_id, product_quantity = count, shipment_date  = date)
    session.add(sm1)
    session.commit()
    print("добавили строку в реестр операций")

# def get_input(input_type:str, username:str, wh:int|str,pr:int|str,q:int,source:int|str) -> dict:
#         if input_type == "CLI":
#             dict_input = get_input_cli(wh,pr,q,source)
#             return dict_input
#
#         if input_type == "Report":
#             dict_input=get_input_Report(wh,pr,q,source)
#             return dict_input
#
# def get_input_cli(wh:int|str, pr:int, q:int, source:int|str):
#     dict_input = {"wh_in":wh,"wh_out":source,"product_id":pr,"count":int(q)}
#     print("get_input_CLI")
#     return dict_input
#
# def get_input_Report(wh:int|str, pr:int, q:int, source:int|str):
#     dict_input = {"wh_in":wh,"wh_out":source,"product_id":pr,"count":int(q)}
#     print("get_input_Report")
#     return dict_input



if __name__ == "__main__":
    main()
