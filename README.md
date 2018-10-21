# BookPro
[ ![Codeship Status for vshelke/bookpro](https://app.codeship.com/projects/7d556770-b50b-0136-511a-46765852e6b0/status?branch=production)](https://app.codeship.com/projects/311351)

[BookPro](https://book-pro.herokuapp.com/) is an open source price comparision tool for books. The tool helps one to search books across multiple sources and get lowest price.
Our current goal is to integrate major book selling sites to provide a wider range of options with a decent looking UI.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
```shell
$ git clone git@github.com:vshelke/bookpro.git
$ cd bookpro/
```

### Develop using virtual environment
```shell
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ ./manage.py runserver 8080
```

### Develop using Docker

```shell
$ docker build -t bookpro .
$ docker run -it -v $(pwd)/bookpro:/app -p 8080:8080 bookpro
```

Now checkout the app at [http://localhost:8080](http://localhost:8080).

## Built With

* [Django](https://www.djangoproject.com/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [Requests](http://docs.python-requests.org/en/master/)

## Contributing

There are many ways through which you can contribute to this project.
* Solving the [issues](https://github.com/vshelke/bookpro/issues). 
* Documentating code following [google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstrings.
* Writing more integrations to the application [here](https://github.com/vshelke/bookpro/tree/master/bookpro/find_books/integrations).
* Submitting bugs [here](https://github.com/vshelke/bookpro/issues) by labelling it as `bug`.
* Use and promote [BookPro](https://book-pro.herokuapp.com/) to get your books for perfect price.

## License
This project is licensed under the GNU LGP License - see the [LICENSE](https://github.com/vshelke/bookpro/blob/master/LICENSE) file for details.
