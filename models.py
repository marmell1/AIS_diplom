from datetime import datetime
#import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Products(Base):
    """Каталог продуктов"""
    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(primary_key=True)
    SKU: Mapped[str] = mapped_column(String(20)) #артикул
    name: Mapped[str] = mapped_column(String(100))
    producer: Mapped[str] = mapped_column(String(100))
    measure: Mapped[str] = mapped_column(String(100)) #ед. измерения
    price: Mapped[int]
    temp: Mapped[int] #температура хранения
    capacity: Mapped[int] #объем - занимает места на складе одна единица товара

    def __repr__(self) -> str:
        return (f"<Products(id={self.id}, "
                f"SKU={self.SKU}, "
                f"name={self.name}, "
                f"price={self.price})>")


class Batches(Base):
    """Партии товаров - перечень всех товаров в каждой партии построчно"""
    __tablename__ = "Batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int]
    product_id: Mapped[int]
    quantity: Mapped[int] #количество штук в партии
    production_date: Mapped[datetime] # дата производства
    purchase_date: Mapped[datetime] # дата покупки
    expiration_date: Mapped[int] # срок годности в днях
    defect: Mapped[int] #количество бракованного товара в штуках
    discount: Mapped[int] #скидка на единицу товара в рублях

    def __repr__(self) -> str:
        return (f"<Batches(id={self.id}, "
                f"batch_id={self.batch_id}, "
                f"product_id={self.product_id}, "
                f"quantity={self.quantity})>")


class Warehouses(Base):
    """Перечень складов"""
    __tablename__ = "Warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[int] # площадь помещения
    conditions: Mapped[int] # температура внутри помещения

    def __repr__(self) -> str:
        return (f"<Warehouses(id={self.id}, "
                f"name={self.name}, ")

class WarehousesLoading(Base):
    """Загрузка складов"""
    __tablename__ = "WarehousesLoading"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int]
    warehouse_name: Mapped[str] = mapped_column(String(100))
    product_id: Mapped[int]
    product_name: Mapped[str] = mapped_column(String(100))
    batch_id: Mapped[int]
    quantity: Mapped[int]
    capacity: Mapped[int] #занимает места

    def __repr__(self) -> str:
        return (f"<WarehousesLoading(id={self.id}, "
                f"warehouse_id={self.warehouse_id}, "
                f"product_id={self.product_id}, "
                f"quantity={self.quantity})>")

class StockMovement(Base):
    """Перемещение ТМЦ"""
    __tablename__ = "StockMovement"

    id: Mapped[int] = mapped_column(primary_key=True)
    input_type: Mapped[str] = mapped_column(String(100)) # тип ввода - CLI или загрузка документа
    input_type_resp: Mapped[str] = mapped_column(String(100)) # ФИО инициатора или номер документа
    source : Mapped[str] = mapped_column(String(100)) # id склада или название поставщика
    destination: Mapped[str] = mapped_column(String(100)) # id склада или название получателя
    product_id: Mapped[int]
    product_quantity: Mapped[int]
    shipment_date: Mapped[datetime] # дата отгрузки

    def __repr__(self) -> str:
        return (f"<WarehousesLoading(id={self.id}, "
                f"warehouse_id={self.warehouse_id}, "
                f"product_id={self.product_id}, "
                f"quantity={self.quantity})>")