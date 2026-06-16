import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração imperativa apontando para o DB de testes via Docker (Porta 5433)
os.environ["DATABASE_URL"] = "postgresql://admin:adminpassword@localhost:5433/test_db"

from main import app, Base, get_db

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def client():
    # Setup: Cria todas as tabelas limpas para o teste
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    # Substitui a dependência injetada no FastAPI
    app.dependency_overrides[get_db] = override_get_db
    
    # Yield devolve o controle para o teste
    with TestClient(app) as test_client:
        yield test_client
        
    # Teardown: Após o teste, destrói o banco, garantindo estado limpo pro próximo
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture()
def produto_existente(client):
    response = client.post("/produtos", json={
        "nome": "Produto Teste", 
        "preco": 99.90, 
        "estoque": 10
    })
    return response.json()