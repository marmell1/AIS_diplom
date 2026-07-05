from models import Products,Warehouses,WarehousesLoading
from database import get_session

def main():
    list_input = get_input("CLI") # читаем источник
    handler(list_input)



    pass

def get_input(input_type)->list:
    if input_type == "CLI":
        get_input_CLI()

    if input_type == "Report":
        get_input_Report()

    list_input = []
    return list_input

def get_input_CLI():
    print("get_input_CLI")

def get_input_Report():
    print("get_input_Report")

def handler(list_input): # берем входящий список
    wh_in = 1
    wh_out = 2
    ip_product = 3
    ip_batch = 4
    count_product = 5

    #with - для  транзакции
    change_wh(wh_out, ip_product,ip_batch,count_product*-1)
    change_wh(wh_in, ip_product,ip_batch,count_product)
    add_stock_movement(wh_in, ip_product,ip_batch,count_product)



def change_wh(wh_in, ip_product,ip_batch,count_product):
    print ("изменяем количество товара на складе")
    # изменяем количество товара на складе
    # плюс проверки по неотрицательным значениям, по наличию такой строки в таблице

def add_stock_movement(wh_in, ip_product,ip_batch,count_product):
    print("добавляем строку в реестр операций")




    '''
    
    
    
    '''

    pass









if __name__ == "__main__":
    main()
