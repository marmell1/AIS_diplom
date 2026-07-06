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

@app.command()
def read(filename):
    """
    Загрузка данных из накладной поставщика. Для примера все два поставщика - ИП Ромашка и ООО Подворье
    """
    workbook = openpyxl.load_workbook(filename, data_only=True)  # data_only=True считывает значения, а не формулы
    sheet = workbook.active
    with get_session() as session1:

        if sheet.cell(row=14, column=9).value == "ИП Ромашка":
            act_number = sheet.cell(row=26, column=50).value
            act_date = sheet.cell(row=26, column=61).value
            input_type_name_date = "Накладная " + act_number + " от " + act_date
            print(act_number, act_date)

            rows = list(sheet.iter_rows(values_only=True))
            # headers = rows[30]

            for row in rows[30:]:
                # row_data = dict(zip(headers, row))
                print()
                print()
                print("***************************row",row)
                print()
                print()
                print(row[0])
                print()
                print()


                if row[0] is not None:
                    print("============", row)
                    print (row[19],row[53])

                    stmt = select(Products.id).where(Products.SKU == row[19])
                    pr_id = session1.scalar(stmt)

                    if pr_id is None:
                        if row[33] == "стандартные":
                            temp = 20
                        elif row[33] == "не выше 10 градусов":
                            temp = 0
                        elif row[33] == "не выше 10 градусов":
                            temp = -20
                        else:
                            temp = "нет данных"



                        product1 = Products(SKU=row[19], name=row[3], producer=row[48],
                                            measure=row[23], price=row[59], temp=temp,
                                            capacity=int(math.ceil(12/row[38])));
                        session1.add(product1)
                        session1.commit()
                        stmt = select(Products.id).where(Products.SKU == row[19])
                        pr_id = session1.scalar(stmt)

                    print("")
                    print("row 38", row[33])
                    print(pr_id)
                    print("")


                    dict_serv = get_input("Report", 1, pr_id, int(row[53]), "ИП Ромашка")
                    print("dict_serv",dict_serv)
                    handler(dict_serv)
                else:
                    break



if __name__ == "__main__":
    app()