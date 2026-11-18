from datetime import date, timedelta
from app import ItemEstoque

def test_alerta_estoque_critico_aaa():
    # Arrange
    item = ItemEstoque(nome_item="Arroz 5kg", categoria="Alimentos", quantidade_atual=3, quantidade_minima=5)
    # Act
    resultado = item.estoque_critico
    # Assert
    assert resultado is True

def test_alerta_validade_proxima_7_dias_aaa():
    # Arrange
    vencimento = date.today() + timedelta(days=5)
    item = ItemEstoque(nome_item="Leite Integral", categoria="Laticinios", quantidade_atual=20, data_validade=vencimento)
    # Act
    resultado = item.validade_proxima
    # Assert
    assert resultado is True
