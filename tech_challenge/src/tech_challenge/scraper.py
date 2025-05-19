import os
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from icecream import ic

from tech_challenge.utils import generate_filename, str_tables_to_int

# Diretório onde os CSVs serão salvos
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
        A função depende da função auxiliar `str_tables_to_int` para converter os nomes
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
    Extrai a primeira tabela HTML com a classe 'tb_base tb_dados' e converte em DataFrame,
    ignorando linhas inválidas e capturando os dados corretamente.

    Args:
        html (str): Conteúdo HTML da página.

    Returns:
        pd.DataFrame: DataFrame contendo os dados da tabela, com cabeçalho extraído da primeira linha.

    Raises:
        AttributeError: Se a tabela esperada não for encontrada no HTML.
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


def salvar_csv(df: pd.DataFrame, filename: str, table_name: str) -> None:
    """
    Salva um DataFrame como arquivo CSV dentro da pasta específica de dados.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        filename (str): Nome do arquivo CSV (ex: "dados.csv").
        table_name (str): Nome da pasta onde o arquivo será salvo dentro de DATA_DIR.

    Returns:
        None
    """
    folder_path = DATA_DIR / table_name

    os.makedirs(folder_path, exist_ok=True)

    full_path = DATA_DIR / table_name / filename

    df.to_csv(full_path, index=False)
    ic(f"Arquivo salvo: {full_path}")


def carregar_csv(filename: str, table_name: str) -> pd.DataFrame:
    """
    Carrega um arquivo CSV local como fallback, realizando limpeza das linhas inválidas.

    Args:
        filename (str): Nome do arquivo CSV a ser carregado.
        table_name (str): Nome da pasta onde o arquivo CSV está localizado dentro de DATA_DIR.

    Returns:
        pd.DataFrame: DataFrame contendo os dados carregados e limpos.

    Raises:
        FileNotFoundError: Se o arquivo CSV especificado não for encontrado no caminho esperado.
    """
    full_path = DATA_DIR / table_name / filename
    if full_path.exists():
        ic(f"Carregando backup local: {full_path}")
        df = pd.read_csv(full_path)

        df = df.dropna(how="all")
        df = df[df.iloc[:, 0].notna()]
        df = df.reset_index(drop=True)

        ic("Backup carregado e limpo com sucesso.")
        return df
    else:
        raise FileNotFoundError(f"Backup não encontrado: {full_path}")


def get_dados_por_aba(
    nome: str, url: str, sub_table: str = None, year: int = None, force: bool = False
) -> pd.DataFrame:
    """
    Obtém os dados de uma aba específica do site da Embrapa com fallback para CSV local.

    A função tenta primeiro carregar o CSV local salvo. Caso não exista ou se `force` for True,
    realiza scraping da página HTML, extrai a tabela, salva o CSV e retorna os dados.

    Args:
        nome (str): Nome identificador da aba (e da pasta/CSV).
        url (str): URL da aba no site da Embrapa.
        sub_table (str, opcional): Nome da sub-tabela (se aplicável).
        year (int, opcional): Ano para filtrar os dados (se aplicável).
        force (bool, opcional): Se True, ignora o CSV local e força scraping direto.

    Returns:
        pd.DataFrame: DataFrame com os dados extraídos ou carregados.

    Raises:
        RuntimeError: Em caso de falha ao obter os dados, seja por scraping ou por ausência do CSV.
    """

    filename = generate_filename(table=nome, sub_table=sub_table, year=year)

    if force:
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            salvar_csv(df, filename, nome)
            return df
        except Exception as e:
            ic(f"[force={force}] Erro ao acessar site da Embrapa: {e}")
            raise RuntimeError(f"Falha ao obter dados da aba '{nome}' (modo forçado).")

    try:
        return carregar_csv(filename, nome)
    except FileNotFoundError:
        try:
            html = fetch_html_from_url(url)
            df = parse_first_table(html)
            salvar_csv(df, filename, nome)
            return df
        except Exception as e:
            ic(f"Erro: {e}")
            raise RuntimeError(f"Dados da aba '{nome}' indisponíveis no momento.")


# --- Funções públicas para uso nos serviços/API --- #


def get_producao_data(year: int = None, force: bool = False) -> pd.DataFrame:
    """
    Obtém os dados de produção da Embrapa para um ano específico, com fallback local e opção de forçar scraping.

    Args:
        year (int, optional): Ano dos dados a serem obtidos. Se None, obtém dados gerais.
        force (bool, optional): Se True, força o scraping do site, ignorando o CSV local.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de produção.
    """
    url = generate_url(table="producao", year=year)
    return get_dados_por_aba(nome="producao", url=url, year=year, force=force)


def get_processamento_data(
    sub_table: str = None, year: int = None, force: bool = False
) -> pd.DataFrame:
    """
    Obtém os dados de processamento da Embrapa para uma sub-tabela e ano específicos,
    com fallback local e opção de forçar scraping.

    Args:
        sub_table (str, optional): Nome da sub-tabela para filtrar os dados.
        year (int, optional): Ano dos dados a serem obtidos.
        force (bool, optional): Se True, força o scraping do site, ignorando o CSV local.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de processamento.
    """
    url = generate_url(table="processamento", year=year, sub_table=sub_table)
    return get_dados_por_aba(
        nome="processamento", url=url, sub_table=sub_table, year=year, force=force
    )


def get_comercializacao_data(year: int = None, force: bool = False) -> pd.DataFrame:
    """
    Obtém os dados de comercialização da Embrapa para um ano específico,
    com fallback local e opção de forçar scraping.

    Args:
        year (int, optional): Ano dos dados a serem obtidos.
        force (bool, optional): Se True, força o scraping do site, ignorando o CSV local.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de comercialização.
    """
    url = generate_url(table="comercializacao", year=year)
    return get_dados_por_aba(nome="comercializacao", url=url, year=year, force=force)


def get_importacao_data(
    sub_table: str = None, year: int = None, force: bool = False
) -> pd.DataFrame:
    """
    Obtém os dados de importação da Embrapa para uma sub-tabela e ano específicos,
    com fallback local e opção de forçar scraping.

    Args:
        sub_table (str, optional): Nome da sub-tabela para filtrar os dados.
        year (int, optional): Ano dos dados a serem obtidos.
        force (bool, optional): Se True, força o scraping do site, ignorando o CSV local.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de importação.
    """
    url = generate_url(table="importacao", year=year, sub_table=sub_table)
    return get_dados_por_aba(
        nome="importacao", url=url, sub_table=sub_table, year=year, force=force
    )


def get_exportacao_data(
    sub_table: str = None, year: int = None, force: bool = False
) -> pd.DataFrame:
    """
    Obtém os dados de exportação da Embrapa para uma sub-tabela e ano específicos,
    com fallback local e opção de forçar scraping.

    Args:
        sub_table (str, optional): Nome da sub-tabela para filtrar os dados.
        year (int, optional): Ano dos dados a serem obtidos.
        force (bool, optional): Se True, força o scraping do site, ignorando o CSV local.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de exportação.
    """
    url = generate_url(table="exportacao", year=year, sub_table=sub_table)
    return get_dados_por_aba(
        nome="exportacao", url=url, sub_table=sub_table, year=year, force=force
    )
