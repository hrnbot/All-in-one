import numpy as np
from .apps import SentimentConfig
import os


def get_analysis(panda_data):
    """
    Get Analysis of CSV Data
    :param panda_data: Panda dataframes
    :return: panda data frames
    """

    # Create Object for Analysis0
    sentiment_object = SentimentConfig.sentiment_object
    ner_object = SentimentConfig.ner_object

    # Get list of sentences
    list = panda_data['text'].to_list()
    sentiment_result = np.array([sentiment_object.get_sentiment(i) for i in list])
    panda_data["Positive Score"] = sentiment_result[:, 2]
    panda_data["Negative Score"] = sentiment_result[:, 0]
    panda_data["Neutral Score"] = sentiment_result[:, 1]
    panda_data["Sentiment Result"] = sentiment_result[:, 3]

    # NER Data Analysis Added
    ner_result = np.array([ner_object.get_ner(i) for i in list])
    panda_data["Entity Result"] = ner_result

    # Adjective Analysis Added
    adjective_result = np.array([ner_object.get_adjectives(i) for i in list])
    panda_data["Adjective Result"] = adjective_result

    return panda_data


def get_analysis_api(panda_data, label):
    """
    Get Analysis of CSV Data from API
    :param panda_data: Panda dataframes
    :type panda_data: pandas dataframes
    :param label: label is from  "positive score", "negative score", "neutral score", "sentiment result", "entity result" and "adjective result"
    :type label:str
    :return: list of result
    :rtype: list
    """
    # Create Object for Analysis
    sentiment_object = SentimentConfig.sentiment_object
    ner_object = SentimentConfig.ner_object

    list = panda_data
    # Get list of sentences
    if label in ["positive score"]:
        sentiment_result = np.array([sentiment_object.get_sentiment(i) for i in list])
        return sentiment_result[:, 2]
    elif label in ["negative score"]:
        sentiment_result = np.array([sentiment_object.get_sentiment(i) for i in list])
        return sentiment_result[:, 0]
    elif label in ["neutral score"]:
        sentiment_result = np.array([sentiment_object.get_sentiment(i) for i in list])
        return sentiment_result[:, 1]
    elif label in ["sentiment result"]:
        sentiment_result = np.array([sentiment_object.get_sentiment(i) for i in list])
        return sentiment_result[:, 3]
    # NER Data Analysis Added
    elif label in ["entity result"]:
        ner_result = np.array([ner_object.get_ner(i) for i in list])
        return ner_result
    # Adjective Analysis Added
    elif label in ["adjective result"]:
        adjective_result = np.array([ner_object.get_adjectives(i) for i in list])
        return adjective_result
    return None


def delete_file(path):
    """Delete file if not available then delete"""
    try:
        os.remove(path)
    except:
        pass


def convert_to_dict(list, startIndex, EndIndex):
    """Convert List to Dictionary and create any index to 0 index"""
    startIndex += 1
    dict = {}
    for i, value in enumerate(list):
        dict[str(startIndex + i)] = str(value)
    return dict
