from models import Products,Warehouses,WarehousesLoading,StockMovement
from database import get_session
from datetime import datetime
from sqlalchemy import select

def main():
    dict_input = get_input("CLI") # читаем источник
    dict_input = {"wh_in":2,"wh_out":1,"product_id":3,"count":10}
    print("test dict")
    handler(dict_input)




def handler(di): # берем входящий dict
    today = datetime.now()
    with get_session() as session:
        add_stock_movement(session, di["wh_in"], di["wh_out"], di["product_id"], di["count"],today.date())
        change_wh(session, di["wh_out"], di["product_id"], (-1*di["count"]))
        change_wh(session, di["wh_in"], di["product_id"], (di["count"]))


        # session.commit()

    #with - для  транзакции
    # change_wh(wh_out, ip_product,ip_batch,count_product*-1)
    # change_wh(wh_in, ip_product,ip_batch,count_product)
    # add_stock_movement(wh_in, ip_product,ip_batch,count_product)



def change_wh(session, wh, product_id, count):
    print ("изменяем количество товара на складе")
    stmt = select(WarehousesLoading).where(WarehousesLoading.warehouse_id == wh, WarehousesLoading.product_id == product_id)
    whl1 = session.scalars(stmt).one_or_none()
    if whl1:
        whl1.quantity += count
        session.commit()
        session.refresh(whl1)


    # изменяем количество товара на складе
    # плюс проверки по неотрицательным значениям, по наличию такой строки в таблице

def add_stock_movement(session, wh_in, wh_out, product_id,count,date):
    print("внесение записи в реестр")

    sm1 = StockMovement(input_type = "test",input_type_resp = "test",source = wh_out,destination = wh_in,
                        product_id = product_id, product_quantity = count, shipment_date  = date)
    session.add(sm1)
    session.commit()
    print("добавили строку в реестр операций")

def get_input(input_type) -> dict:
        if input_type == "CLI":
            get_input_CLI()

        if input_type == "Report":
            get_input_Report()

        dict_input = {}
        return dict_input

def get_input_CLI():
        print("get_input_CLI")

def get_input_Report():
        print("get_input_Report")



if __name__ == "__main__":
    main()
