# BookPro
[ ![Codeship Status for vshelke/bookpro](https://app.codeship.com/projects/7d556770-b50b-0136-511a-46765852e6b0/status?branch=master)](https://app.codeship.com/projects/311351)

Book shopping comparision tool!

# Develop locally using a virtual environment

```shell
$ git clone git@github.com:vshelke/bookpro.git
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ cd bookpro
$ pip3 install -r requirements.txt
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py collectstatic
$ ./manage.py runserver 8080
```

# Develop with Docker

```shell
$ cd bookpro/
$ docker build -t bookpro .
$ docker run -it -v $(pwd)/bookpro:/app -p 8080:8080 bookpro
```

Now browse to `localhost:8080` and see the app.

# Contributing

* add more integrations for different e-commerce websites.

