from _4_Processing import get_input as get_input
from _4_Processing import handler as handler
from database import get_session
from models import Products
from sqlalchemy import select
import math

import openpyxl

import typer
app = typer.Typer()

@app.command()
def move (wh: int = typer.Option(..., help="Склад, на который перемещаем либо покупатель"),
          pr: int = typer.Option(..., help="Товар, который перемещаем"),
          q: int = typer.Option(..., help="Количество товара"),
          source: int = typer.Option(..., help="Склад, с которого списываем либо поставщик")):
    """
    Добавление товара на склад - ввести номер склада, id продукта, количество, склад-источник
    """
    #создать если нет такого продукта
    dict_serv = get_input("CLI", wh,pr,q,source)
    handler(dict_serv)

    print(f"Внесли склад номер {wh}, товар {pr}, {q} ед., источник - {source}")

def check_temp(rr):
    if rr == "стандартные":
        temp = 20
    elif rr == "не выше 10 градусов":
        temp = 0
    elif rr == "заморозка":
        temp = -20
    else:
        temp = "нет данных"
    return temp

@app.command()
def read(filename, wh_id):
    """
    Загрузка данных из накладной поставщика. Для примера всего два поставщика - ИП Ромашка и ООО Подворье
    """
    workbook = openpyxl.load_workbook(filename, data_only=True)  # data_only=True считывает значения, а не формулы
    sheet = workbook.active

    with get_session() as session1:

        dic_vendors = {"ИП Ромашка":1,"ООО Подворье":2}
        dic_bill_check_vendor_row={1:14,2:1}
        dic_bill_check_vendor_column={1:9,2:1}
        dic_bill_number_row={1:26,2:3}
        dic_bill_number_column={1:50,2:2}
        dic_bill_number_date_row={1:26,2:2}
        dic_bill_number_date_column={1:61,2:1}
        dic_bill_first_row={1:30,2:5}
        dic_bill_sku_column={1:19,2:0}
        dic_bill_name_column={1:3,2:1}
        dic_bill_products_quantity_column={1:53,2:5}
        dic_bill_producer_column={1:48,2:2}
        dic_bill_measure_column={1:23,2:4}
        dic_bill_price_column1={1:59,2:6}
        dic_bill_price_column2={2:5}
        dic_bill_temp_column={1:33,2:3}
        dic_bill_capacity_column1={1:38,2:7}
        dic_bill_capacity_column2={2:5}

        for key in dic_vendors.keys():
            if sheet.cell(row=dic_bill_check_vendor_row[dic_vendors[key]], column=dic_bill_check_vendor_column[dic_vendors[key]]).value == key:
                act_number = sheet.cell(row=dic_bill_number_row[dic_vendors[key]], column=dic_bill_number_column[dic_vendors[key]]).value
                act_date = sheet.cell(row=dic_bill_number_date_row[dic_vendors[key]], column=dic_bill_number_date_column[dic_vendors[key]]).value
                input_type_name_date = "Накладная " + act_number + " от " + act_date
                print(act_number, act_date)

                rows = list(sheet.iter_rows(values_only=True))
                for row in rows[dic_bill_first_row[dic_vendors[key]]:]:
                    if row[0] is not None:
                        stmt = select(Products.id).where(Products.SKU == row[dic_bill_sku_column[dic_vendors[key]]])
                        pr_id = session1.scalar(stmt)
                        if pr_id is None:
                            temp = check_temp(row[dic_bill_temp_column[dic_vendors[key]]])
                            if dic_vendors[key] ==1:
                                price = row[dic_bill_price_column1[dic_vendors[key]]]
                                capacity = int(math.ceil(12 / row[dic_bill_capacity_column1[dic_vendors[key]]]))

                            if dic_vendors[key] ==2:
                                price = int(round(row[dic_bill_price_column1[dic_vendors[key]]]/row[dic_bill_price_column2[dic_vendors[key]]]))
                                capacity = int(math.ceil(row[dic_bill_capacity_column1[dic_vendors[key]]] / row[dic_bill_capacity_column2[dic_vendors[key]]]))

                            product1 = Products(SKU=row[dic_bill_sku_column[dic_vendors[key]]],
                                                name=row[dic_bill_name_column[dic_vendors[key]]],
                                                producer=row[dic_bill_producer_column[dic_vendors[key]]],
                                                measure=row[dic_bill_measure_column[dic_vendors[key]]],
                                                price=price,
                                                temp=temp,
                                                capacity=capacity)
                            session1.add(product1)
                            session1.commit()
                            stmt = select(Products.id).where(Products.SKU == row[dic_bill_sku_column[dic_vendors[key]]])
                            pr_id = session1.scalar(stmt)
                        dict_serv = get_input("Report", wh_id, pr_id, int(row[dic_bill_products_quantity_column[dic_vendors[key]]]), "ИП Ромашка")
                        handler(dict_serv)
                    else:
                        break




        #
        # if sheet.cell(row=14, column=9).value == "ИП Ромашка":
        #
        #     act_number = sheet.cell(row=26, column=50).value
        #     act_date = sheet.cell(row=26, column=61).value
        #     input_type_name_date = "Накладная " + act_number + " от " + act_date
        #     print(act_number, act_date)
        #
        #     rows = list(sheet.iter_rows(values_only=True))
        #     for row in rows[30:]:
        #         if row[0] is not None:
        #             stmt = select(Products.id).where(Products.SKU == row[19])
        #             pr_id = session1.scalar(stmt)
        #             if pr_id is None:
        #                 temp = check_temp(row[33])
        #                 product1 = Products(SKU=row[19], name=row[3], producer=row[48],
        #                                     measure=row[23], price=row[59], temp=temp,
        #                                     capacity=int(math.ceil(12/row[38])));
        #                 session1.add(product1)
        #                 session1.commit()
        #                 stmt = select(Products.id).where(Products.SKU == row[19])
        #                 pr_id = session1.scalar(stmt)
        #             dict_serv = get_input("Report", wh_id, pr_id, int(row[53]), "ИП Ромашка")
        #             handler(dict_serv)
        #         else:
        #             break
        #
        # if sheet.cell(row=1, column=1).value == "ООО Подворье":
        #     act_number = sheet.cell(row=3, column=2).value
        #     act_date = sheet.cell(row=2, column=1).value
        #     input_type_name_date = "Накладная " + act_number + " от " + act_date
        #     print(act_number, act_date)
        #
        #     rows = list(sheet.iter_rows(values_only=True))
        #     for row in rows[5:]:
        #         if row[0] is not None:
        #             stmt = select(Products.id).where(Products.SKU == row[0])
        #             pr_id = session1.scalar(stmt)
        #             if pr_id is None:
        #                 temp = check_temp(row[3])
        #                 product1 = Products(SKU=row[0], name=row[1], producer=row[2],
        #                                     measure=row[4], price=int(round(row[6]/row[5])), temp=temp,
        #                                     capacity=int(math.ceil(row[7]/row[5])));
        #                 session1.add(product1)
        #                 session1.commit()
        #                 stmt = select(Products.id).where(Products.SKU == row[0])
        #                 pr_id = session1.scalar(stmt)
        #             dict_serv = get_input("Report", wh_id, pr_id, int(row[5]), "ООО Подворье")
        #             handler(dict_serv)
        #         else:
        #             break














if __name__ == "__main__":
    app()