from tech_challenge import scraper

def get_dados_aba(aba: str):
    """
    Retorna os dados da aba solicitada usando a camada de scraping.

    Args:
        aba (str): Nome da aba (producao, processamento, etc.)

    Returns:
        pd.DataFrame: Dados da aba.
    """
    match aba:
        case "producao":
            return scraper.get_producao_data()
        case "processamento":
            return scraper.get_processamento_data()
        case "comercializacao":
            return scraper.get_comercializacao_data()
        case "importacao":
            return scraper.get_importacao_data()
        case "exportacao":
            return scraper.get_exportacao_data()
        case _:
            raise ValueError("Aba inválida.")
