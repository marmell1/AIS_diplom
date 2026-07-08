import pytest
from Money import Money

# 1. Тест базового позитивного сценария
def test_Money_101kop():
    money1 = Money(100,120)
    assert money1.rub == 101
    assert money1.kop == 20


    """
    проверить конвертацию температуры
    
    проверить выбрасывает ли ошибку при ошибке
    
    """