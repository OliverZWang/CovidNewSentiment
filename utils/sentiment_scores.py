
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import statistics

'''
A model that computes the VADER sentiment scores of an article both as a long String and by sentence

Arguments:

    article:                The content of an article as a String
    

Attributes:

    scores_by_article: A dictionary of VADER scores with keys of 'neg', 'neu', 'pos', and 'compound'
    compound_by_article: The compound score value of the previous attribute (scores_by_article)
    average_sentence: The average of the sentiment scores of all sentences
    median_sentence: The median of the sentiment scores of all sentences
    mode_sentence: The mode of the sentiment scores of all sentences
    pstd_sentence: The population standard deviation of the sentiment scores of all sentences

Methods:

    result_dict:                Returns a dictionary of class attributes mapped to their values

Example:

    article = "FDA Delays Emergency Vaccine Approval Until They Finish Evaluating New Bagged Salad Kit. Clarifying that the federal agency would take a look at Pfizer’s submission eventually, the FDA announced Friday that it would delay the emergency coronavirus vaccine approval until they were finished evaluating a bagged salad kit. "
    article_scores = SentimentScores(article)
    print(article_scores.compound_by_article)

    score_dict = article_scores.result_dict()
    print(score_dict)


'''



class SentimentScores():

    def __init__(self, article):
        self.article = article
        self.sid = SentimentIntensityAnalyzer()
        self.scores_by_article = self.sid.polarity_scores(article)
        self.compound_by_article = self.scores_by_article['compound']

        self.scores_by_sentence = self.compute_sentence_scores()
        self.average_sentence = statistics.mean(self.scores_by_sentence)
        self.median_sentence = statistics.median(self.scores_by_sentence)
        self.mode_sentence = statistics.mode(self.scores_by_sentence)
        self.pstd_sentence = statistics.pstdev(self.scores_by_sentence)

    def result_dict(self):
        sentiment_scores = {
            "scores_by_article": self.scores_by_article,
            "compound_by_article": self.compound_by_article,
            "average_sentence": self.average_sentence,
            "median_sentence": self.median_sentence,
            "mode_sentence": self.mode_sentence,
            "pstd_sentence": self.pstd_sentence
        }
        return sentiment_scores

    
    # FROM: https://github.com/iLtc/NLP2590/blob/qiuhao/EDA.ipynb
    def get_sentences(self, article):
        article = str(article)
        article = article.replace('\xa0', '\n')
        sentences = re.split(r"\.|\?|\!", article)
        sentences = [sentence.replace("\\", "") for sentence in sentences]
        return sentences

    def compute_sentence_scores(self):
        sentences = self.get_sentences(self.article)
        scores = []
        for sentence in sentences:
            scores.append(self.sid.polarity_scores(sentence)['compound'])
        return scores











