FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y git curl python3.7
RUN mkdir upload_video
ADD . upload_video/
WORKDIR upload_video
RUN pip install django
RUN pip install djangorestframework
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]


