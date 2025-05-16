import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from icecream import ic
from pathlib import Path

# Diretório onde os CSVs serão salvos
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# URLs das abas da Embrapa
URLS = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "importacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "exportacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
}

def fetch_html_from_url(url: str) -> str:
    """Tenta acessar a URL da Embrapa e retorna o HTML da página."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ic(f"Acesso bem-sucedido à URL: {url}")
        return response.text
    except requests.RequestException as e:
        ic(f"Erro ao acessar {url}: {e}")
        raise

def parse_first_table(html: str) -> pd.DataFrame:
    """
    Extrai a primeira tabela presente no HTML,
    ignorando linhas inválidas.
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = pd.read_html(str(soup))
    df = tables[0]
    
    df = df.dropna(how="all")
    df = df[df.iloc[:, 0].notna()]
    df = df.reset_index(drop=True)

    ic("Tabela extraída e limpa com sucesso.")
    return df


def salvar_csv(df: pd.DataFrame, nome_arquivo: str) -> None:
    """Salva um DataFrame como CSV na pasta data/."""
    caminho = DATA_DIR / nome_arquivo
    df.to_csv(caminho, index=False)
    ic(f"Arquivo salvo: {caminho}")

def carregar_csv(nome_arquivo: str) -> pd.DataFrame:
    """
    Carrega um CSV local como fallback, limpando linhas inválidas.

    Args:
        nome_arquivo (str): Nome do arquivo CSV.

    Returns:
        pd.DataFrame: Dados carregados e limpos.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    caminho = DATA_DIR / nome_arquivo
    if caminho.exists():
        ic(f"Carregando backup local: {caminho}")
        df = pd.read_csv(caminho)

        # Limpeza: remove linhas com valores nulos em colunas obrigatórias
        df = df.dropna(how="all")  # remove linhas completamente vazias
        df = df[df.iloc[:, 0].notna()]  # remove linhas com a 1ª coluna vazia
        df = df.reset_index(drop=True)

        ic("Backup carregado e limpo com sucesso.")
        return df
    else:
        raise FileNotFoundError(f"Backup não encontrado: {caminho}")

def get_dados_por_aba(nome: str, url: str, force: bool = False) -> pd.DataFrame:
    """
    Lógica genérica para scraping com fallback CSV por aba.
    
    Args:
        nome (str): Nome identificador da aba (e do CSV).
        url (str): URL da aba no site da Embrapa.
        force (bool): Se True, ignora CSV e tenta scraping direto.
    """
    nome_arquivo = f"{nome}.csv"

    if force:
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            salvar_csv(df, nome_arquivo)
            return df
        except Exception as e:
            ic(f"[force={force}] Erro ao acessar site da Embrapa: {e}")
            raise RuntimeError(f"Falha ao obter dados da aba '{nome}' (modo forçado).")

    try:
        return carregar_csv(nome_arquivo)
    except FileNotFoundError:
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            salvar_csv(df, nome_arquivo)
            return df
        except Exception as e:
            ic(f"Erro: {e}")
            raise RuntimeError(f"Dados da aba '{nome}' indisponíveis no momento.")

# --- Funções públicas para uso nos serviços/API --- #

def get_producao_data(force: bool = False) -> pd.DataFrame:
    return get_dados_por_aba("producao", URLS["producao"], force)

def get_processamento_data(force: bool = False) -> pd.DataFrame:
    return get_dados_por_aba("processamento", URLS["processamento"], force)

def get_comercializacao_data(force: bool = False) -> pd.DataFrame:
    return get_dados_por_aba("comercializacao", URLS["comercializacao"], force)

def get_importacao_data(force: bool = False) -> pd.DataFrame:
    return get_dados_por_aba("importacao", URLS["importacao"], force)

def get_exportacao_data(force: bool = False) -> pd.DataFrame:
    return get_dados_por_aba("exportacao", URLS["exportacao"], force)
