import re


def _to_pascal_case(name: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", name)
    return "".join(w.capitalize() for w in words)


def _to_snake_case(name: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", name)
    return "_".join(w.lower() for w in words)
