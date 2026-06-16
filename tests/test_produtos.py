import pytest

# 1. Listar quando o banco está vazio
def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

# 2. Criar e verificar persistência
def test_criar_produto_persistencia(client):
    payload = {"nome": "Teclado Mecânico", "preco": 350.50, "estoque": 5}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Teclado Mecânico"
    assert "id" in data

# 3. Criar e verificar que aparece na listagem
def test_criar_e_listar(client):
    client.post("/produtos", json={"nome": "Mouse Gamer", "preco": 120.0, "estoque": 2})
    response = client.get("/produtos")
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Mouse Gamer"

# 4. Buscar produto por id - Sucesso
def test_buscar_produto_por_id_sucesso(client, produto_existente):
    id = produto_existente["id"]
    response = client.get(f"/produtos/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id

# 5. Buscar produto com id inexistente - 404
def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/999")
    assert response.status_code == 404

# 6. Deletar produto - Retorna 204
def test_deletar_produto_sucesso(client, produto_existente):
    id = produto_existente["id"]
    response = client.delete(f"/produtos/{id}")
    assert response.status_code == 204

# 7. Deletar e confirmar remoção com GET
def test_deletar_e_confirmar_remocao(client, produto_existente):
    id = produto_existente["id"]
    client.delete(f"/produtos/{id}")
    
    response = client.get(f"/produtos/{id}")
    assert response.status_code == 404

# 8. Deletar produto inexistente - 404
def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/999")
    assert response.status_code == 404

# 9. Teste Parametrizado (Status 422 - Unprocessable Entity)
@pytest.mark.parametrize("payload_invalido", [
    {"nome": "", "preco": 10.0},        # Nome vazio
    {"nome": "Falta preco", "estoque": 5}, # Ausência de campo obrigatório (preco)
    {"nome": "Preco zero", "preco": 0.0},  # Preço inválido (=0)
    {"nome": "Preco negativo", "preco": -15.0} # Preço inválido (<0)
])
def test_criar_produto_payloads_invalidos(client, payload_invalido):
    response = client.post("/produtos", json=payload_invalido)
    assert response.status_code == 422

# 10. Isolamento de Estado
def test_isolamento_de_estado_entre_testes(client):
    # Prova de Isolamento: mesmo após executar `produto_existente` ou `client.post` em testes 
    # passados (ou se rodar fora de ordem), o setup `drop_all`/`create_all` na fixture garante banco limpo.
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == [] # O banco DEVE estar vazio no início desta execução