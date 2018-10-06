# tubedl


## Online video downloader <http://tubedl.herokuapp.com/>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Tube DL is a website for downloading videos from sites like YouTube.com.
It is built on top of [rg3/youtube-dl](https://github.com/rg3/youtube-dl), the [Django framework](https://github.com/django/django) and works for both Python2 and Python3.

![Screenshot](https://raw.github.com/AndreMiras/tubedl/master/docs/tubedl.png)

## Install
Production environment:
```sh
pip install -r requirements.txt
```
Development environment:
```sh
pip install -r requirements/dev.txt
```

## Run
With Gunicorn WSGI server:
```sh
gunicorn tubedl.wsgi
```
With Django development server:
```sh
python manage.py runserver
```

## Tests
Using Django test framework only:
```sh
python manage.py test
```
Using Tox:
```sh
tox
```
