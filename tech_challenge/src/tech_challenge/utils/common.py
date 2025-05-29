import math

def parse_quantity(value: str | int | float | None) -> int | None:
    """
    Converte um valor que representa quantidade para um inteiro, tratando casos especiais.

    Args:
        value (str | int | None): Valor a ser convertido. Pode ser uma string com pontos como separadores
            de milhar, um inteiro ou None. Strings contendo apenas "-" são interpretadas como None.

    Returns:
        int | None: Valor convertido para inteiro, ou None se o valor for "-" ou None.
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return int(value)

    if isinstance(value, str):
        value = value.strip()
        if value in ["-", "", "nan", "NaN"]:
            return None
        try:
            return int(value.replace(".", "").replace(",", ""))
        except ValueError:
            return None

    return None