import re

import ftfy


price_re = re.compile('(\d+.\d+)')


def price_format(price):
    if not price:
        return 0

    if isinstance(price, str):
        return float(price_re.search(price.replace(',', '')).group(1))
    return price


def price_sale_format(price, sale_price):
    price = price_format(price)
    sale_price = price_format(sale_price)
    return 0 if not price or not sale_price or price == sale_price else sale_price


def fix_text(text):
    return ftfy.fix_text(text)
