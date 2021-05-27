# FAQ Chatbot 

##Purpose:
To obtain the sentiment score based on the uploaded Sentence/s in a
[CSV](https://drive.google.com/file/d/1Hub3qYAT3NQh2CvbjOwSdWOMbPkd5c4r/view?usp=drivesdk).
### Input

CSV File with a fixed format
  - Unique key
  - Comment content
  - Etc.

### Output
CSV file should retain all fields in the input file plus following additional data:
- Sentiment Scores
    - Positive sentiment likelihood
    - Neutral sentiment likelihood
    - Negative sentiment likelihood (summed three likelihood should be 100%)
    - Sentiment label(i.e. Positive, Neutral, Negative)
- Adjectives in the sentence (all adjectives containing in content)
- Entity Keywords 
  - Person 
  - Norp
  - Facility
  - Organization
  - GPE
  - Countryv
  - City
  - Religion
  - Location
  - Product
  - Event 
  - Work of Art
  - Law
  - Language
  - Date
  - Time
  - Duration
  - Percent
  - Money
  - Quantity
  - Ordinal
  - Cardinal

- A very simple website (no design is needed) for us to upload the csv file to try, and the website should return the
  result as a download file in csv format
- A dashboard to retrieve a CSV file through Date Filters
- An API to retrieve a CSV File

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
conda activate env_name
python manage.py runserver
```

## Create SuperUser
```
python manage.py createsuperuser
```

## Postman API
[Postman collection:](https://www.getpostman.com/collections/9bf76896d023f39b242a)

[Post API Documentation:](https://documenter.getpostman.com/view/8895684/TzRX9RR1)