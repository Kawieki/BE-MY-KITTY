def parse_value(val):
    """
        Parsuje wartość wejściową na odpowiedni typ danych.

        Args:
            val (str): Wartość wejściowa w formie ciągu znaków.

        Returns:
            Union[int, float, tuple[int], bool, str]: Parsowana wartość w odpowiednim typie danych.
    """
    val = val.strip()
    if ',' in val:
        try:
            return tuple(map(int, val.split(',')))
        except ValueError:
            return val
    elif val.lower() in ("true", "false"):
        return val.lower() == "true"
    else:
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val
