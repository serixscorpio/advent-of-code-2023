def read_lines(file_name: str, delimiter: str = None) -> list[str]:
    with open(file_name) as file:
        if delimiter:
            return file.read().split(delimiter)
        return file.read().splitlines()
