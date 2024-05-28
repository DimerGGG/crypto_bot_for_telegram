import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество валюты должно быть числом.")

        url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException("Ошибка при запросе к API обмена валют.")

        # Используем библиотеку json для парсинга ответа
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            raise APIException("Ошибка при обработке ответа от API.")

        if quote.upper() not in data['rates']:
            raise APIException(f"Валюта {quote} не найдена.")
        if base.upper() not in data['rates']:
            raise APIException(f"Валюта {base} не найдена.")

        rate = data['rates'][quote.upper()]
        total_base = rate * amount

        return total_base