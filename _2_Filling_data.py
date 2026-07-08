from models import Products,Warehouses,WarehousesLoading
from database import get_session

def main():
    with get_session() as session:
        print("Добавление товаров в каталог")
        product1 = Products(SKU = "а000001", name="Вода негазированная 1,5 литра", producer = "БонАква",
                            measure = "шт",price = 80,temp = 22,
                            capacity = 2);
        product2 = Products(SKU = "а000002", name="Вода газированная 0,5 литра", producer = "БонАква",
                            measure = "шт",price = 50,temp = 22,
                            capacity = 1);
        product3 = Products(SKU = "а000003", name="Молоко 1 литр", producer = "Княгинино",
                            measure = "шт",price = 85,temp = 10,
                            capacity = 2);
        product4 = Products(SKU = "а000004", name="Пельмени замороженные", producer = "Мираторг",
                            measure = "шт",price = 300,temp = -10,
                            capacity = 2);
        product5 = Products(SKU = "а000005", name="Креветки замороженные", producer = "Русское море",
                            measure = "кг",price = 1500,temp = -15,
                            capacity = 2);
        product6 = Products(SKU = "а000006", name="Индейка охлажденная", producer = "Индилайт",
                            measure = "кг",price = 800,temp = 5,
                            capacity = 2);
        product7 = Products(SKU = "а000007", name="Вода негазированная 5 литров", producer = "Аква",
                            measure = "шт",price = 200,temp = 22,
                            capacity = 5);
        product8 = Products(SKU = "а000008", name="Вода негазированная 20 литров", producer = "Аква",
                            measure = "шт",price = 450,temp = 22,
                            capacity = 15);


        wh1 = Warehouses(name="Главный - приемка", capacity = 500, conditions = 20);
        wh2 = Warehouses(name="Холодильный склад", capacity = 750, conditions = 0);
        wh3 = Warehouses(name="Морозильный склад", capacity = 600, conditions = -20);
        wh4 = Warehouses(name="Склад 1", capacity = 500, conditions = 20);
        wh5 = Warehouses(name="Склад 2", capacity = 500, conditions = 20);
        wh6 = Warehouses(name="Склад 3", capacity = 500, conditions = 20);
        wh7 = Warehouses(name="Отбраковка", capacity = 400, conditions = 10);


        whl1 = WarehousesLoading(warehouse_id = 1,warehouse_name = "",product_id = 1,product_name = "",quantity = 10,capacity = 0)
        whl2 = WarehousesLoading(warehouse_id = 1,warehouse_name = "",product_id = 2,product_name = "",quantity = 15,capacity = 0)
        whl3 = WarehousesLoading(warehouse_id = 1,warehouse_name = "",product_id = 8,product_name = "",quantity = 30,capacity = 0)
        whl4 = WarehousesLoading(warehouse_id = 2,warehouse_name = "",product_id = 3,product_name = "",quantity = 5,capacity = 0)
        whl5 = WarehousesLoading(warehouse_id = 3,warehouse_name = "",product_id = 5,product_name = "",quantity = 15,capacity = 0)
        whl6 = WarehousesLoading(warehouse_id = 4,warehouse_name = "",product_id = 6,product_name = "",quantity = 5,capacity = 0)
        whl7 = WarehousesLoading(warehouse_id = 4,warehouse_name = "",product_id = 7,product_name = "",quantity = 12,capacity = 0)
        whl8 = WarehousesLoading(warehouse_id = 6,warehouse_name = "",product_id = 8,product_name = "",quantity = 10,capacity = 0)
        whl9 = WarehousesLoading(warehouse_id = 7,warehouse_name = "",product_id = 5,product_name = "",quantity = 2,capacity = 0)
        whl10 = WarehousesLoading(warehouse_id = 7,warehouse_name = "",product_id = 6,product_name = "",quantity = 3,capacity = 0)


        session.add_all([product1,product2,product3,product4,product5,product6,product7,product8])
        session.add_all([wh1,wh2,wh3,wh4,wh5,wh6,wh7])
        session.add_all([whl1,whl2,whl3,whl4,whl5,whl6,whl7,whl8,whl9,whl10])

        session.commit()

if __name__ == "__main__":
    main()
