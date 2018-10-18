# BookPro
[ ![Codeship Status for vshelke/bookpro](https://app.codeship.com/projects/7d556770-b50b-0136-511a-46765852e6b0/status?branch=master)](https://app.codeship.com/projects/311351)

Book Shopping comparision system!!

# Develop locally

```cd bookpro/```

```pip install -r requirements.txt```

```./manage.py runserver 8080```

# Develop with Docker

```cd bookpro/```

```docker build -t bookpro .```

```docker run -it -v $(pwd)/bookpro:/app -p 8080:8080 bookpro```

# Contributing

* add more integrations for different e-commerce websites.

