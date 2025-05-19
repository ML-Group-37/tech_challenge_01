from typing import Optional


def parse_quantity(value: str | int | None) -> int | None:
    """
    Converte um valor que representa quantidade para um inteiro, tratando casos especiais.

    Args:
        value (str | int | None): Valor a ser convertido. Pode ser uma string com pontos como separadores
            de milhar, um inteiro ou None. Strings contendo apenas "-" são interpretadas como None.

    Returns:
        int | None: Valor convertido para inteiro, ou None se o valor for "-" ou None.
    """
    if isinstance(value, str):
        if value.strip() == "-":
            return None
        return int(value.replace(".", ""))
    return value


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


def generate_filename(
    table: str, sub_table: Optional[str] = None, year: Optional[int] = None
) -> str:
    """
    Gera o nome do arquivo CSV baseado nos parâmetros de tabela, sub-tabela e ano.

    Args:
        table (str): Nome da tabela principal.
        sub_table (Optional[str], opcional): Nome da sub-tabela. Padrão é None.
        year (Optional[int], opcional): Ano dos dados. Padrão é None.

    Returns:
        str: Nome do arquivo CSV gerado no formato apropriado, por exemplo:
            - "producao_vinifera_2023.csv"
            - "producao_vinifera.csv"
            - "producao_2023.csv"
            - "producao.csv"
    """

    if sub_table and year:
        return f"{table}_{sub_table}_{year}.csv"
    if sub_table:
        return f"{table}_{sub_table}.csv"
    if year:
        return f"{table}_{year}.csv"

    return f"{table}.csv"
