# BookPro
[ ![Codeship Status for vshelke/bookpro](https://app.codeship.com/projects/7d556770-b50b-0136-511a-46765852e6b0/status?branch=production)](https://app.codeship.com/projects/311351)

[BookPro](https://book-pro.herokuapp.com/) is a price comparision tool for books on multiple e-commerce websites. It helps you get the best deals for your favourite books right away.

## Features

* Get cheapest price for your favourite book.

## Develop locally using a virtual environment

```shell
$ git clone git@github.com:vshelke/bookpro.git
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ cd bookpro
$ pip3 install -r requirements.txt
$ ./manage.py runserver 8080
```

## Develop with Docker

```shell
$ cd bookpro/
$ docker build -t bookpro .
$ docker run -it -v $(pwd)/bookpro:/app -p 8080:8080 bookpro
```

Now checkout the app at [http://localhost:8080](http://localhost:8080).

## Contributing

Check out our [contributing guide](https://github.com/vshelke/bookpro/blob/master/CONTRIBUTING.md) for more details.

