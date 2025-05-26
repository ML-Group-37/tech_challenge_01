from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from icecream import ic

from tech_challenge.utils.db import load_data_from_db, save_data_in_db

URL_PREFIX = "http://vitibrasil.cnpuv.embrapa.br/index.php?"


def generate_url(table: str, sub_table: int = None, year: int = None) -> str:
    """
    Gera a URL para acessar uma tabela específica no site da Embrapa, considerando
    opcionalmente uma sub-tabela e um ano.

    Args:
        table (str): Nome da tabela principal (exemplo: "producao").
        sub_table (int, optional): Identificador numérico da sub-tabela (exemplo: 2).
            Pode ser None se não houver sub-tabela.
        year (int, optional): Ano desejado para consulta. Pode ser None para omitir.

    Returns:
        str: URL completa formatada para acesso à tabela desejada no site da Embrapa.

    Nota:
        A função depende da função auxiliar str_tables_to_int para converter os nomes
        das tabelas em seus identificadores numéricos correspondentes.
    """

    int_table, int_sub_table = str_tables_to_int(table, sub_table)

    if sub_table and year:
        url_suffix = (
            f"ano={year}&opcao=opt_0{int_table}&subopcao=subopt_0{int_sub_table}"
        )
    elif sub_table:
        url_suffix = f"subopcao=subopt_0{int_sub_table}&opcao=opt_0{int_table}"
    elif year:
        url_suffix = f"ano={year}&opcao=opt_0{int_table}"
    else:
        url_suffix = f"opcao=opt_0{int_table}"

    url = f"{URL_PREFIX}{url_suffix}"

    return url


def fetch_html_from_url(url: str) -> str:
    """
    Tenta acessar a URL fornecida e retorna o conteúdo HTML da página.

    Args:
        url (str): Endereço da página web a ser acessada.

    Returns:
        str: Conteúdo HTML da página acessada.

    Raises:
        requests.RequestException: Se ocorrer algum erro durante a requisição HTTP.
    """
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
    Extrai a primeira tabela HTML com a classe 'tb_base tb_dados' e converte em um DataFrame.

    A função localiza a primeira tabela HTML com a classe específica, extrai os dados,
    e os organiza em um DataFrame. O cabeçalho da tabela é extraído da primeira linha,
    e as linhas subsequentes são usadas como dados.

    Args:
        html (str): Conteúdo HTML da página.

    Returns:
        pd.DataFrame: DataFrame contendo os dados da tabela, com cabeçalho extraído da primeira linha.

    Raises:
        AttributeError: Se a tabela esperada não for encontrada no HTML.
        ValueError: Se a tabela encontrada não contiver dados suficientes para criar um DataFrame.
    """
    soup = BeautifulSoup(html, "html.parser")
    html_table = soup.find("table", {"class": "tb_base tb_dados"})

    rows = html_table.find_all("tr")
    data = []

    for row in rows:
        cells = row.find_all(["th", "td"])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        data.append(cells_text)

    df = pd.DataFrame(data[1:], columns=data[0])
    ic("Tabela extraída e limpa com sucesso.")
    return df


def get_dados_por_aba(
    nome: str, url: str, sub_table: str = None, year: int = None, force: bool = False
) -> pd.DataFrame:
    """
    Obtém os dados de uma aba específica do site da Embrapa com fallback para o banco de dados local.

    A função tenta primeiro carregar os dados do banco de dados local. Caso não existam ou se `force` for True,
    realiza scraping da página HTML, extrai a tabela, salva os dados no banco e retorna os dados.

    Args:
        nome (str): Nome identificador da aba (e da tabela no banco de dados).
        url (str): URL da aba no site da Embrapa.
        sub_table (str, opcional): Nome da sub-tabela (se aplicável).
        year (int, opcional): Ano para filtrar os dados (se aplicável).
        force (bool, opcional): Se True, ignora o banco de dados local e força scraping direto.

    Returns:
        pd.DataFrame: DataFrame com os dados extraídos ou carregados.

    Raises:
        RuntimeError: Em caso de falha ao obter os dados, seja por scraping ou por ausência no banco de dados.
    """

    if force:
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            save_data_in_db(df=df, table=nome, year=year, sub_table=sub_table)
            return df
        except Exception as e:
            ic(f"[force={force}] Erro ao acessar site da Embrapa: {e}")
            raise RuntimeError(f"Falha ao obter dados da aba '{nome}' (modo forçado).")

    try:
        return load_data_from_db(table=nome, year=year, sub_table=sub_table)
    except Exception as e:
        ic(
            f"Dados para {nome}_{sub_table}_{year} não encontrados no banco de dados: {e}"
        )
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            save_data_in_db(df=df, table=nome, year=year, sub_table=sub_table)
            return df
        except Exception as e:
            ic(f"Erro: {e}")
            raise RuntimeError(f"Dados da aba '{nome}' indisponíveis no momento.")


def str_tables_to_int(str_table: str, sub_table: Optional[str] = None) -> int:
    """
    Converte o nome da tabela e sub-tabela em seus respectivos códigos inteiros usados pela Embrapa.

    Args:
        str_table (str): Nome da tabela principal (ex: "producao").
        sub_table (Optional[str], opcional): Nome da sub-tabela (ex: "Viníferas"). Padrão é None.

    Returns:
        tuple[int, Optional[int]]: Tupla contendo o código inteiro da tabela principal e,
        se aplicável, o código da sub-tabela. Se não houver sub-tabela, o segundo valor é None.

    Raises:
        ValueError: Se o nome da tabela principal ou da sub-tabela for inválido.
    """

    table_mapping = {
        "producao": 2,
        "processamento": 3,
        "comercializacao": 4,
        "importacao": 5,
        "exportacao": 6,
    }

    sub_table_mapping = {
        "producao": {},
        "processamento": {
            "Viníferas": 1,
            "Americanas e híbridas": 2,
            "Uvas de mesa": 3,
            "Sem classificação": 4,
        },
        "comercializacao": {},
        "importacao": {
            "Vinhos de mesa": 1,
            "Espumantes": 2,
            "Uvas frescas": 3,
            "Uvas passas": 4,
            "Suco de uva": 5,
        },
        "exportacao": {
            "Vinhos de mesa": 1,
            "Espumantes": 2,
            "Uvas frescas": 3,
            "Suco de uva": 4,
        },
    }

    if str_table in table_mapping:
        int_table = table_mapping[str_table]
    else:
        raise ValueError(f"Invalid table name: {str_table}")

    if sub_table and str_table in sub_table_mapping:
        if sub_table in sub_table_mapping[str_table]:
            int_sub_table = sub_table_mapping[str_table][sub_table]
        else:
            raise ValueError(
                f"Invalid sub-table name: {sub_table} for table {str_table}"
            )

        return int_table, int_sub_table
    else:
        return int_table, None
