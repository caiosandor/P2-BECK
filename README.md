Projeto: API de E-commerce com FastAPI, Pytest e Docker
Este projeto consiste em uma API de gerenciamento de produtos, desenvolvida com FastAPI e SQLAlchemy, utilizando PostgreSQL via Docker para persistência e Pytest para testes automatizados.

1. Instruções para subir o banco de teste com Docker
O projeto utiliza dois bancos de dados isolados (desenvolvimento e testes). Para provisioná-los corretamente, você precisa do Docker Desktop rodando no seu computador.

No terminal do PowerShell, na raiz do projeto (onde está o arquivo docker-compose.yml), execute o seguinte comando:

PowerShell
docker-compose up -d
Isso iniciará os contêineres em segundo plano. O banco de testes estará disponível na porta 5433 e o banco de desenvolvimento na porta 5432.

Dica: Se aparecer um aviso amarelo sobre "version is obsolete", você pode ignorá-lo ou apagar a primeira linha (version: '3.8') do seu arquivo docker-compose.yml.

2. Preparando o Ambiente Python
A API roda localmente, então você precisa de um ambiente virtual com as dependências instaladas antes de rodar os testes.

No PowerShell, crie e ative o ambiente virtual:

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
(O indicador (venv) deve aparecer verde no terminal).

Em seguida, instale as dependências:

PowerShell
pip install fastapi "uvicorn[standard]" httpx pytest
3. Comando exato para executar os testes
Certifique-se de que o seu ambiente virtual (venv) está ativado e que o Docker está rodando. Execute o seguinte comando no terminal:

PowerShell
pytest -v
(A flag -v serve para mostrar a saída detalhada, listando o nome de cada teste executado).

4. Saída esperada do pytest
Após rodar o comando acima, a saída no seu terminal indicará 100% de sucesso nos 13 testes e se parecerá exatamente com isto:

Plaintext
========================================================================= test session starts ==========================================================================
platform win32 -- Python 3.13.12, pytest-9.1.0, pluggy-1.6.0 -- C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\caios\OneDrive\Desktop\P2 BECK
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.0
collected 13 items                                                                                                                                                       

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED                                                                                                  [  7%]
tests/test_produtos.py::test_criar_produto_persistencia PASSED                                                                                                   [ 15%]
tests/test_produtos.py::test_criar_e_listar PASSED                                                                                                               [ 23%]
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED                                                                                                [ 30%]
tests/test_produtos.py::test_buscar_produto_inexistente PASSED                                                                                                   [ 38%]
tests/test_produtos.py::test_deletar_produto_sucesso PASSED                                                                                                      [ 46%]
tests/test_produtos.py::test_deletar_e_confirmar_remocao PASSED                                                                                                  [ 53%]
tests/test_produtos.py::test_deletar_produto_inexistente PASSED                                                                                                  [ 61%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido0] PASSED                                                                          [ 69%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido1] PASSED                                                                          [ 76%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido2] PASSED                                                                          [ 84%]
tests/test_produtos.py::test_criar_produto_payloads_invalidos[payload_invalido3] PASSED                                                                          [ 92%]
tests/test_produtos.py::test_isolamento_de_estado_entre_testes PASSED                                                                                            [100%]

=========================================================================== warnings summary ===========================================================================
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

main.py:35
  C:\Users\caios\OneDrive\Desktop\P2 BECK\main.py:35: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    class ProdutoOut(ProdutoBase):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
==================================================================== 13 passed, 2 warnings in 0.46s ====================================================================
(Nota: Os "warnings" na saída são apenas avisos de depreciação futura das bibliotecas e não representam erros na aplicação).

5. Saída esperada do pytest --cov=main --cov-report=term-missing -v
Após rodar o comando acima, a saída no seu terminal indicará 100% de sucesso nos 13 testes e se parecerá exatamente com isto:

(venv) PS C:\Users\caios\OneDrive\Desktop\P2 BECK> pytest --cov=main --cov-report=term-missing -v
========================================================================= test session starts ==========================================================================
platform win32 -- Python 3.13.12, pytest-9.1.0, pluggy-1.6.0 -- C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\caios\OneDrive\Desktop\P2 BECK
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.0, cov-7.1.0
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
  C:\Users\caios\OneDrive\Desktop\P2 BECK\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

main.py:35
  C:\Users\caios\OneDrive\Desktop\P2 BECK\main.py:35: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    class ProdutoOut(ProdutoBase):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================ tests coverage ============================================================================
___________________________________________________________ coverage: platform win32, python 3.13.12-final-0 ___________________________________________________________

Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py      58      4    93%   46-50
---------------------------------------
TOTAL        58      4    93%
==================================================================== 13 passed, 2 warnings in 0.65s ====================================================================

6. Breve explicação do isolamento entre testes
Para garantir que o estado de um teste não afete o resultado do próximo (o que causaria falsos positivos ou falsos negativos), o projeto utiliza Fixtures do Pytest com Injeção de Dependências:

Redirecionamento (Dependency Override): No arquivo conftest.py, a função app.dependency_overrides força a API a se conectar ao banco de testes (porta 5433), ignorando o banco de desenvolvimento.

Setup limpo: Antes de cada teste individual começar, a fixture recria todas as tabelas vazias utilizando Base.metadata.create_all.

Execução: O comando yield pausa a fixture e permite que o teste específico rode com um banco 100% limpo.

Teardown rigoroso: Imediatamente após o teste acabar, o código após o yield entra em ação rodando Base.metadata.drop_all, que apaga todas as tabelas e dados criados. Isso garante que o banco volte a ficar completamente limpo para a execução do próximo teste da fila.