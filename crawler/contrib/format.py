import re

import ftfy


price_re = re.compile('(\d+.\d+)')


def price_format(price):
    if not price:
        return 0

    if isinstance(price, str):
        return float(price_re.search(price.replace(',', '')).group(1))
    return price


def fix_text(text):
    return ftfy.fix_text(text)
