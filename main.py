import os
from dotenv import load_dotenv
import requests


def is_bitlink(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
                            headers=headers)
    return response.ok


def count_clicks(token, bitlink):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        params = (
            ('unit', 'day'),
            ('units', '-1'),
        )
        response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary', headers=headers,
                                params=params)
        response.raise_for_status()
        total_clicks = response.json()['total_clicks']
        return f'Вы ввели битлинк. Сумма кликов по данному битлинку: {total_clicks}'

    except requests.exceptions.HTTPError as err:
        if err.response.status_code==402:
            return f'Вы ввели битлинк. Подсчет количество кликов не входит в ваш тарифный план на Bitly'


def shorten_link(token, link):
    try:
        response_link = requests.post(link)
        response_link.raise_for_status()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        params = {"long_url": link}
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=params)
        response.raise_for_status()
        bitlink = response.json()['id']
        return f'Вы ввели ссылку. Битлинк этого сайта: {bitlink}'
    except requests.exceptions.ConnectionError:
        return f'Ссылка "{link}" не открывается'


def main():
    token = os.environ['BITLY_TOKEN']
    user_input = input("Введите ссылку или битлинк: ")
    try:
        if is_bitlink(token, user_input):
            print(count_clicks(token, user_input))
        else:
            print(shorten_link(token, user_input))
    except requests.exceptions.ConnectionError:
        print(f'Проверьте соединение и повторите попытку')


if __name__ == '__main__':
    load_dotenv()
    main()