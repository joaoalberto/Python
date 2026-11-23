"""Process Goodreads-style bookshelf exports into complete series lists."""
from collections import Counter
import re


IGNORED_SHELVES = {
    "to-read",
    "amazon",
    "kobo",
    "googlebooks",
    "tor",
    "ibooks",
    "currently-reading",
    "collections",
}


def separar_series(lines):
    """Split each input line into book/shelf tokens.

    Commas and whitespace are both accepted as separators. Brackets and quotes
    are stripped to support lines such as ``[to-read, amazon, series-2]``.
    """
    tokens = []
    for line in lines:
        for token in re.split(r"[\s,]+", line.strip()):
            token = token.strip("[](){}'\"` ")
            if token:
                tokens.append(token)
    return tokens


def extrair_max_series(series):
    """Return (series name, expected book count) for a slug ending in -N."""
    name, separator, count = series.rpartition("-")
    if not separator or not name or not count.isdigit():
        return None
    return name, int(count)


def processar_linhas(lines):
    """Return complete series as ``series-name,count`` strings.

    A series is complete when its observed token count exactly matches the
    number at the end of its slug, preserving the original script's behavior.
    """
    books = separar_series(lines)
    counts = Counter(books)
    unique_series = sorted(
        book for book in counts if book not in IGNORED_SHELVES
    )

    complete = []
    for slug in unique_series:
        parsed = extrair_max_series(slug)
        if parsed is None:
            continue
        name, expected_count = parsed
        observed_count = counts[slug]
        if observed_count == expected_count:
            complete.append(f"{name},{observed_count}")
    return complete


def ler_arquivo(arquivo):
    """Read a UTF-8 text file and return its lines."""
    with open(arquivo, "r", encoding="utf-8-sig") as file:
        return file.readlines()


def gravar_arquivo(arquivo, linhas):
    """Write non-empty lines to a UTF-8 text file."""
    with open(arquivo, "w", encoding="utf-8") as file:
        for linha in linhas:
            if linha.strip():
                file.write(linha.rstrip() + "\n")


if __name__ == "__main__":
    input_file = "bookshelves.txt"
    output_file = "series_completas.txt"
    results = processar_linhas(ler_arquivo(input_file))
    gravar_arquivo(output_file, results)
    print(f"Series completas encontradas: {len(results)}")
