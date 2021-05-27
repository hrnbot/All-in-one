"""This File will contains all third party Class and object which needs to be initialied only once """
from django.apps import AppConfig
import numpy as np
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import spacy


def list_to_string(array, separator):
    """
    Convert List,Tupples,Set into string separaated by "separator"
    :param array: List, Tupple or Set
    :param separator: Separator which can use to separate all values of array
    :type separator:str
    :return: String converted from list, If list empty then Nan
    :rtype: str
    """
    if len(array) > 0:
        return separator.join(map(str, array))
    return "NaN"  # if there is nothing array then return "NaN"


class Sentiment():
    def __init__(self):
        """
        Class will use cardiffnlp twitter for sentiment analysis
        """
        # Default Configuration of CardiffNLP"
        self.task = 'sentiment'
        self.MODEL = f"cardiffnlp/twitter-roberta-base-{self.task}"
        self.labels = ['Negative', 'Neutral', 'Positive']
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = TFAutoModelForSequenceClassification.from_pretrained(self.MODEL)

    def get_sentiment(self, sentence):
        """
        Returns Sentimental Score of sentence
        :param sentence: sentence of which sentiment score is needed
        :type sentence: str
        :return: negative_score, neutral_score, positive_score, sentiment label
        :rtype: float,float,float,str
        """
        encoded_input = self.tokenizer(sentence, return_tensors='tf')
        output = self.model(encoded_input)
        scores = output[0][0].numpy()
        scores = softmax(scores)
        return np.array([scores[0], scores[1], scores[2], self.labels[np.argmax(scores)]])


class NER():
    def __init__(self):
        """
        This Class will help in detection of NER and Adjactive
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.adjective = ["ADJ"]

    def get_ner(self, sentence):
        """
        Used to Extract Named Entities from a sentence
        :param sentence: Sentence whose Entity need to extract
        :type sentence: str
        :return: Entities like PERSON;PERSON;PERCENT
        :rtype: str
        """
        doc = self.nlp(sentence)
        return list_to_string([i.label_ for i in doc.ents], ";")

    def get_adjectives(self, sentence):
        """
        Used to Extract Adjectives from a sentence
        :param sentence: sentence from where adjective need to be extracted
        :type sentence: str
        :return: Adjectives like nice;happy;fun;good;easy
        :rtype: str
        """
        doc = self.nlp(sentence)
        tags = []
        for token in doc:
            if token.pos_ in self.adjective:
                tags.append(token.text)
        return list_to_string(set(tags), ";")



class SentimentConfig(AppConfig):
    """  Singleton Instance for Singleton class Object """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sentiment'
    sentiment_object = Sentiment()
    ner_object = NER()
