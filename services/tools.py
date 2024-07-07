import re
from datetime import date, datetime


def parse_dates(date_str: str, year: int) -> date:
    """
    Parse date string in format YYYY-MM-DD from vintage's column title
    Each vintage have a date in format like 'на 16 января'
    """

    # Clean
    date_str = date_str.replace("*", "").lstrip("на ")

    month_mapping = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12,
    }

    parts = date_str.split()
    day = int(parts[0])
    month_name = parts[1]

    month = month_mapping[month_name]

    date_obj = datetime(year, month, day).date()

    return date_obj


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and underscores)
    and converts spaces to hyphens. Also strips leading and trailing whitespace.
    """
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value


def transliterate(name):
    """
    Автор: LarsKort
    Дата: 16/07/2011; 1:05 GMT-4;
    https://gist.github.com/ledovsky/6398962
    """
    # Слоаврь с заменами
    dictionary = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "cz",
        "ш": "sh",
        "щ": "scz",
        "ъ": "",
        "ы": "y",
        "ь": "b",
        "э": "e",
        "ю": "u",
        "я": "ja",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "ZH",
        "З": "Z",
        "И": "I",
        "Й": "I",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "H",
        "Ц": "C",
        "Ч": "CZ",
        "Ш": "SH",
        "Щ": "SCH",
        "Ъ": "",
        "Ы": "y",
        "Ь": "b",
        "Э": "E",
        "Ю": "U",
        "Я": "YA",
        ",": ",",
        "?": "?",
        " ": "_",
        "~": "~",
        "!": "!",
        "@": "@",
        "#": "#",
        "$": "$",
        "%": "%",
        "^": "^",
        "&": "&",
        "*": "*",
        "(": "(",
        ")": ")",
        "-": "-",
        "=": "=",
        "+": "+",
        ":": ":",
        ";": ";",
        "<": "<",
        ">": ">",
        "'": "'",
        '"': '"',
        "\\": "\\",
        "/": "/",
        "№": "#",
        "[": "[",
        "]": "]",
        "{": "{",
        "}": "}",
        "ґ": "r",
        "ї": "r",
        "є": "e",
        "Ґ": "g",
        "Ї": "i",
        "Є": "e",
        "—": "-",
    }

    # Циклически заменяем все буквы в строке
    for key in dictionary:
        name = name.replace(key, dictionary[key])
    return name


def slugify_cyrillic_word(word: str) -> str:
    return slugify(transliterate(word))
