tubedl
======


Online video downloader <http://tubedl.herokuapp.com/>
--------------

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Tube DL is a website for downloading videos from sites like YouTube.com.
It is built on top of [rg3/youtube-dl](https://github.com/rg3/youtube-dl) and Django framework.

![Screenshot](https://raw.github.com/AndreMiras/tubedl/master/docs/tubedl.png)

Install
--------------
```
pip install -r requirements.txt
```

Run
--------------
With Gunicorn WSGI server:
```
gunicorn tubedl.wsgi
```
With Django development server:
```
python manage.py runserver
```

Tests
--------------
Using Django test framework only:
```
python manage.py test
```
Using Tox:
```
tox
```
