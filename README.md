# URL shortener

Консольная утилита для сокращения ссылок с помощью сервиса [bit.ly](https://bit.ly).


### Установка необходимых библиотек
```
$ pip install -r requirements.txt
```

### Настройка окружения
[Токен API Bitly](https://bitly.is/accesstoken) записать в переменную окружения `BITLY_GENERIC_TOKEN`

### Пример `.env` файла:
```
BITLY_GENERIC_TOKEN=<TOKEN>
```


### Запуск
```
$ python3 script.py <url>
```
