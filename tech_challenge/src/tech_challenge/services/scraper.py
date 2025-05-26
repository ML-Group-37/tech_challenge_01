import pandas as pd

from tech_challenge.utils.scraper import (
    generate_url,
    get_dados_por_aba,
)


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
