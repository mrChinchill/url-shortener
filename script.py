#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError


API_URL = 'https://api-ssl.bitly.com'


def cut_scheme(url):
    url_parsed = urlparse(url)
    scheme = '{}://'.format(url_parsed.scheme)
    return url_parsed.geturl().replace(scheme, '', 1)


def shorten_link(token, link):
    url = '{host}/v4/shorten'.format(host=API_URL)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    payload = {'long_url': link}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token, link):
    url = '{host}/v4/bitlinks/{bitlink}/clicks/summary'.format(
        host=API_URL,
        bitlink=cut_scheme(link)
    )
    headers = {'Authorization': 'Bearer {}'.format(token)}
    payload = {
        'unit': 'month',
        'units': -1
    }

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()['total_clicks']


def bitlink_exist(token, link):
    url = '{host}/v4/bitlinks/{bitlink}'.format(
        host=API_URL,
        bitlink=cut_scheme(link)
    )
    headers = {'Authorization': 'Bearer {}'.format(token)}

    response = requests.get(url, headers=headers)

    return response.ok


def main():
    load_dotenv()
    token = os.getenv('BITLY_GENERIC_TOKEN', '')

    user_input = input('Введите ссылку: ')

    try:
        if bitlink_exist(token, user_input):
            clicks_count = count_clicks(token, user_input)
            print('По вашей ссылке прошли: {} раз(а)'.format(clicks_count))
        else:
            bitlink = shorten_link(token, user_input)
            print('Битлинк: {}'.format(bitlink))

    except HTTPError as exception:
        if exception.response.status_code == 403:
            print('Ошибка доступа.')
        if exception.response.status_code in (400, 404):
            print('Некорректная ссылка.')

    except ConnectionError:
        print('Ошибка соединения.')


if __name__ == '__main__':
    main()
