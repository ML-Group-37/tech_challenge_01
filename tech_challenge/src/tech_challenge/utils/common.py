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
