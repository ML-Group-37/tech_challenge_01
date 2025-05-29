import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def auth_token():
    """Gera um token JWT válido após registrar e autenticar o usuário de teste."""
    payload = {"username": "test_user", "password": "123456"}

    # Cadastro (ignora se já existir)
    requests.post(f"{BASE_URL}/register", json=payload)

    # Login
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 200, "Falha no login"
    data = response.json()
    assert "access_token" in data
    return data["access_token"]


def test_read_root():
    """Verifica se o endpoint raiz '/' retorna status 200 e resposta com chave 'nome'."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "nome" in response.json()


def test_producao_endpoint(auth_token):
    """Testa o endpoint '/producao' com token JWT válido."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/producao?year=2023", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_processamento_endpoint(auth_token):
    """Testa o endpoint '/processamento' com token e subtabela 'Viníferas'."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(
        f"{BASE_URL}/processamento?sub_table=Viníferas&year=2023",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_comercializacao_endpoint(auth_token):
    """Testa o endpoint '/comercializacao' com token JWT."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/comercializacao?year=2023", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_importacao_endpoint(auth_token):
    """Testa o endpoint '/importacao' com subtabela 'Vinhos de mesa'."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(
        f"{BASE_URL}/importacao?sub_table=Vinhos de mesa&year=2023",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_exportacao_endpoint(auth_token):
    """Testa o endpoint '/exportacao' com subtabela 'Vinhos de mesa'."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(
        f"{BASE_URL}/exportacao?sub_table=Vinhos de mesa&year=2023",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
