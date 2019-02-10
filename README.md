# tubedl

[![Build Status](https://travis-ci.com/AndreMiras/tubedl.svg?branch=develop)](https://travis-ci.com/AndreMiras/tubedl)

## Online video downloader <http://tubedl.herokuapp.com/>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Tube DL is a website for downloading videos from sites like YouTube.com.
It is built on top of [rg3/youtube-dl](https://github.com/rg3/youtube-dl), the [Django framework](https://github.com/django/django) and works for both Python2 and Python3.

![Screenshot](https://raw.github.com/AndreMiras/tubedl/master/docs/tubedl.png)

## Install
Production environment:
```sh
make virtualenv
```
You also need system requirements e.g. for merging video/audio:
```sh
make system_dependencies
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
```sh
make test
```
