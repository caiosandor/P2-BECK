# API de E-commerce (FastAPI + Pytest + Docker)

Este projeto consiste em uma API de gerenciamento de produtos desenvolvida com FastAPI e SQLAlchemy, utilizando PostgreSQL via Docker para persistência de dados e Pytest para testes automatizados.

---

## 1. Instruções para subir os bancos de dados (Docker)

O projeto utiliza dois bancos de dados isolados (desenvolvimento e testes). Para provisioná-los, é necessário ter o Docker Desktop em execução.

No PowerShell, abra a raiz do projeto (onde está o `docker-compose.yml`) e execute:

```powershell
docker-compose up -d
Isso iniciará os contêineres em segundo plano. O banco de testes estará disponível na porta 5433 e o banco de desenvolvimento na porta 5432.

A API e os testes rodam localmente. É necessário configurar um ambiente virtual (venv) para isolar as dependências.

No PowerShell, crie e ative a venv:

python -m venv venv
.\venv\Scripts\Activate.ps1

Com o ambiente ativado (o indicador (venv) aparecerá no terminal), instale as dependências:

pip install fastapi "uvicorn[standard]" httpx pytest pytest-cov

Certifique-se de que a venv está ativada e o Docker está rodando. Para executar a suíte de testes, utilize:

pytest -v

Saída esperada do pytest

========================================================================= test session starts ==========================================================================
platform win32 -- Python 3.13.12, pytest-9.1.0, pluggy-1.6.0 -- C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\caios\OneDrive\Desktop\P2 BECK
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.0
collected 13 items

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED                                                                                                   [  7%]
tests/test_produtos.py::test_criar_produto_persistencia PASSED                                                                                                    [ 15%]
tests/test_produtos.py::test_criar_e_listar PASSED                                                                                                                [ 23%]
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED                                                                                                 [ 30%]
tests/test_produtos.py::test_buscar_produto_inexistente PASSED                                                                                                    [ 38%]
tests/test_produtos.py::test_deletar_produto_sucesso PASSED                                                                                                       [ 46%]
tests/test_produtos.py::test_deletar_e_confirmar_remocao PASSED                                                                                                   [ 53%]
tests/test_produtos.py::test_deletar_produto_inexistente PASSED                                                                                                   [ 61%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido0] PASSED                                                                           [ 69%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido1] PASSED                                                                           [ 76%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido2] PASSED                                                                           [ 84%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido3] PASSED                                                                           [ 92%]
tests/test_produtos.py::test_isolamento_de_estado_entre_testes PASSED                                                                                             [100%]

=========================================================================== warnings summary ===========================================================================
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.
    from starlette.testclient import TestClient as TestClient  # noqa

main.py:35
  C:\Users\caios\OneDrive\Desktop\P2 BECK\main.py:35: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use `ConfigDict` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at [https://errors.pydantic.dev/2.13/migration/](https://errors.pydantic.dev/2.13/migration/)
    class ProdutoOut(ProdutoBase):

-- Docs: [https://docs.pytest.org/en/stable/how-to/capture-warnings.html](https://docs.pytest.org/en/stable/how-to/capture-warnings.html)
==================================================================== 13 passed, 2 warnings in 0.46s ====================================================================




Para verificar a cobertura do código principal, execute:

pytest --cov=main --cov-report=term-missing -v


A saída gerará a tabela de cobertura, indicando 93% de cobertura do arquivo main.py:

Plaintext
============================================================================ tests coverage ============================================================================
___________________________________________________________ coverage: platform win32, python 3.13.12-final-0 ___________________________________________________________
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py      58      4    93%   46-50
---------------------------------------
TOTAL        58      4    93%
==================================================================== 13 passed, 2 warnings in 0.65


Para garantir que o estado de um teste não afete o resultado do próximo (evitando falsos positivos ou negativos), o projeto utiliza Fixtures do Pytest com Injeção de Dependências. O fluxo ocorre da seguinte forma:

Redirecionamento (Dependency Override): No arquivo conftest.py, a função app.dependency_overrides força a API a se conectar ao banco de testes (porta 5433), ignorando o banco de desenvolvimento.

Setup limpo: Antes de cada teste iniciar, a fixture recria todas as tabelas zeradas utilizando Base.metadata.create_all.

Execução: O comando yield pausa a fixture e permite que o teste específico seja executado em um banco de dados 100% limpo.

Teardown rigoroso: Imediatamente após a conclusão do teste, o código retoma a execução a partir do yield e aciona o comando Base.metadata.drop_all, apagando todas as tabelas e dados criados. Isso garante que o banco esteja completamente zerado para o próximo teste da fila.
