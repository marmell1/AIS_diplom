from _4_Processing import get_input as get_input
from _4_Processing import handler as handler

import typer
app = typer.Typer()

@app.command()
def move (wh, pr, q, source):
    """
    Добавление товара на склад - ввести номер склада, id продукта, количество
    """
    #создать если нет такого продукта
    dict = get_input("CLI", wh,pr,q,source)
    handler(dict)

    print(f"Внесли склад номер {wh}, товар {pr}, {q} ед., источник - {source}")

#
#
# @app.command()
# def move(text):
#     """
#     Перемещение товара со склада на склад
#     """
#     print(f"Ввели {text}")
#
# @app.command()
# def delete(text):
#     """
#     Удаление товара со склада
#     """
#     print(f"Ввели {text}")

if __name__ == "__main__":
    app()