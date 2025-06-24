from config import CURRENCY_RATES

user_currency = {}

def get_user_currency(user_id):
    return user_currency.get(user_id, "USD")

def set_user_currency(user_id, currency):
    user_currency[user_id] = currency

def convert_price(price_usd, currency):
    rate = CURRENCY_RATES.get(currency, 1)
    return round(price_usd * rate, 2)
