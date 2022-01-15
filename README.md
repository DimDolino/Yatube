# yamdb_final
yamdb_final - проект реализации интерфейса api_yamdb, который  собирает отзывы пользователей на произведения, через Docker-Compose с использованием workflow, с деплоем на сервере

### Используемые технологии:

+ Django,
+ Django rest framework,
+ Docker-Compose,
+ Python
+ Workflow

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```python
git clone https://github.com/DimDolino/yamdb_final.git
```
В файле yamdb_final/infra/.env укажите собственные данные:

```python
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Подготовить удаленный сервер:

1. Остановить службу nginx, если она запущена:

```python
 sudo systemctl stop nginx
```
2. Выполнить установку docker.io:

```python
 sudo systemd stop nginx
```
3. Выполнить установку docker-compose:
https://docs.docker.com/compose/install/

4. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

5. Скопируйте также на удаленный сервер файл фикстур fixtures.json из yamdb_final/infra/:

```python
csp fixtures.json username@server_id
```

6. После выполнения workflow перейти на удаленный сервер и, далее:

Выполнить миграции:

```bash
sudo docker-compose exec web python manage.py migrate
```
Для создания суперпользователя выполнить команду:

```bash
sudo docker-compose exec web python manage.py createsuperuser
```
Для сбора статики проекта выполнить:

```bash
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
## Добавляем данные в контейнер:

Скопировать данные в образ:

```bash
sudo docker cp fixtures.json <id_контейнера web>:/app
```


Выполнить команду:
```bash
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
### Автор:

+ Семёнов Дмитрий

![example workflow](https://github.com/dimdolino/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Ссылка на сайт:
http://51.250.28.166