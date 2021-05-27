# FAQ Chatbot 
Do Sentiment Analysis, NER Detection and Adjective Detection

## Installation
```bash
git clone repo
conda create -n sentiment python=3.7
conda activate sentiment
pip install -r requirements.txt
conda install cudatoolkit=10.1 cudnn=7.6.5
python -m spacy download en
sudo apt-get install rabbitmq-server
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
 ```


## RUN
```bash
conda activate 
python manage.py runserver
```

## Create SuperUser
```
python manage.py createsuperuser
```