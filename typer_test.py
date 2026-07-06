import typer

# Инициализируем приложение Typer
app = typer.Typer()

# Регистрируем функцию как команду CLI
@app.command()
def user_info(
    name: str,
    age: int,
    is_admin: bool = False
):
    """
    Выводит информацию о пользователе.
    """
    status = "Администратор" if is_admin else "Пользователь"
    print(f"Привет, {name}! Возраст: {age}. Статус: {status}")

# Точка входа для запуска из терминала
if __name__ == "__main__":
    app()