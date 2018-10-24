FROM python:3.6.6-slim

WORKDIR /app
ADD ./bookpro/requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD bookpro/ /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
