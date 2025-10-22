from forex_python.converter import CurrencyRates

c = CurrencyRates()
amount = 100
from_currency = 'USD'
to_currency = 'EUR'
converted_amount = c.convert(from_currency, to_currency, amount)
print(f"{amount} {from_currency} = {converted_amount} {to_currency}")