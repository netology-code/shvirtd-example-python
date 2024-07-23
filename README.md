# Домашнее задание к занятию 5. «Практическое применение Docker»


## Задача 0 ##

Установлены соответствующие версии пакетов:
```
damir@dz5:~$ docker --version
Docker version 27.0.3, build 7d4bcd8
damir@dz5:~$ docker compose version
Docker Compose version v2.28.1
```


## Задача 1 ##

Форк репозитария создан, создан dockerfile (Dockerfile.python), образ собирается, при этом файл requirements.txt копируется в образ для дальнейшей настройки окружения.
В .dockerignore указаны все файлы, не имеющие отношения к сборке образа.


## Задача 2 (*) ##

Отчет о сканировании тут: https://github.com/Granit16/shvirtd-example-python/blob/next/vulnerabilities.csv


## Задача 3 ##

Файл compose.yaml создан, файл "proxy.yaml" продключен к нему с помощью директивы "include".
Образ приложения web собирается из файла Dockerfile.python, все остальные параметры соответствуют заданию.
Переменные в приложение передаются через файл .env и/или через переменные окружения в разделе environment.

Приложение db создается в соответсвии с заданными параметрами, переменные для создания пароля root, БД и данных пользователя передаются через файл .env.

После запуска приложений команда curl выдает ожидаемый результат:
```
damir@dz5:~/rrr/shvirtd-example-python$ curl -L http://127.0.0.1:8090
TIME: 2024-07-23 09:55:59, IP: 127.0.0.1damir@dz5:~/rrr/shvirtd-example-python$
```

Результат подключения к контейнур с БД и выполенения запроса представлен на скриншоте:
![alt text](https://github.com/Granit16/shvirtd-example-python/blob/next/SQL.png?raw=true)


