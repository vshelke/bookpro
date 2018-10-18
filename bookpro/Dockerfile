from python:3.6-alpine3.6
add . /app
workdir /app
run apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt && \
 apk --purge del .build-deps
cmd ["./manage.py", "runserver", "0.0.0.0:8080"]
