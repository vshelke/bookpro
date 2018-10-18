from python:3.6.6-slim
add bookpro /app
workdir /app
run pip install -r requirements.txt 
cmd ["./manage.py", "runserver", "0.0.0.0:8080"]
