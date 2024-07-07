import re
from datetime import datetime, date


def parse_dates(date_str: str, year: int) -> date:
    """
        Parse date string in format YYYY-MM-DD from vintage's column title
        Each vintage have a date in format like 'на 16 января'
    """

    # Clean
    date_str = date_str.replace("*", "").lstrip("на ")

    month_mapping = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
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
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value
