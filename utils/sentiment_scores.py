
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import statistics

'''
A model that computes the VADER sentiment scores of an article both as a long String and by sentence, 
which also allows updates of certain words' Vader scores. 

Arguments:

    article:                The content of an article as a String
    new_words(optional):    A dictionary with updated scores for words
    

Attributes:

    scores_by_article:      A dictionary of VADER scores with keys of 'neg', 'neu', 'pos', and 'compound'
    compound_by_article:    The compound score value of the previous attribute (scores_by_article)
    average_sentence:       The average of the sentiment scores of all sentences
    median_sentence:        The median of the sentiment scores of all sentences
    mode_sentence:          The mode of the sentiment scores of all sentences
    pstd_sentence:          The population standard deviation of the sentiment scores of all sentences
    avg_first_last_para: The average of scores of the first and last paragraph

Methods:

    result_dict:                Returns a dictionary of class attributes mapped to their values

Example:

    article = "FDA Delays Emergency Vaccine Approval Until They Finish Evaluating New Bagged Salad Kit. Clarifying that the federal agency would take a look at Pfizer’s submission eventually, the FDA announced Friday that it would delay the emergency coronavirus vaccine approval until they were finished evaluating a bagged salad kit. "
    new_words = {'negative': 2}
    article_scores = SentimentScores(article, new_words=new_words)
    print(article_scores.compound_by_article)

    score_dict = article_scores.result_dict()
    print(score_dict)


'''

NEW_WORDS = {"crisis": 0, "positive": -1, "great": 0, "authority": -2, "Crisis": 0, "Positive": -1, "Great": 0, "Authority": -2, "coronavirus": -1, "pandemic": 0.5, "outbreak": -1.5, "virus": -1, "lockdown": -1, "trump": -1.5, "Coronavirus": -1, "Pandemic": 0.5, "Outbreak": -1.5, "Virus": -1, "Lockdown": -1, "Trump": -1.5, "TRUMP": -1.5}

class SentimentScores():

    def __init__(self, article, *args, **kwargs):
        self.article = article
        self.sid = SentimentIntensityAnalyzer()

        if 'new_words' in kwargs.keys():
            self.sid.lexicon.update(kwargs['new_words'])
        else:
            self.sid.lexicon.update(NEW_WORDS)

        self.scores_by_article = self.sid.polarity_scores(article)
        self.compound_by_article = self.scores_by_article['compound']

        self.scores_by_sentence = self.compute_sentence_scores()
        self.average_sentence = statistics.mean(self.scores_by_sentence)
        self.median_sentence = statistics.median(self.scores_by_sentence)
        self.mode_sentence = statistics.mode(self.scores_by_sentence)
        self.pstd_sentence = statistics.pstdev(self.scores_by_sentence)

        self.scores_by_paragraph = self.compute_paragraph_scores()
        self.average_paragraph = statistics.mean(self.scores_by_paragraph)
        self.median_paragraph = statistics.median(self.scores_by_paragraph)
        self.mode_paragraph = statistics.mode(self.scores_by_paragraph)
        self.pstd_paragraph = statistics.pstdev(self.scores_by_paragraph)

        self.avg_first_last_para = self.scores_by_paragraph[0] + self.scores_by_paragraph[-1]
        
    def result_dict(self):
        sentiment_scores = {
            # "scores_by_article": self.scores_by_article,
            "compound_by_article": self.compound_by_article,
            "average_sentence": self.average_sentence,
            "median_sentence": self.median_sentence,
            "mode_sentence": self.mode_sentence,
            "pstd_sentence": self.pstd_sentence,
            "average_paragraph": self.average_paragraph,
            "median_paragraph": self.median_paragraph,
            "mode_paragraph": self.mode_paragraph,
            "pstd_paragraph": self.pstd_paragraph,
            "avg_first_last_para": self.avg_first_last_para
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

    def get_paragraphs(self, article):
        article = str(article)
        article = article.replace('\xa0', '\n')
        paragraphs = re.split('\n', article)
        paragraphs = [paragraph.replace('\\', '') for paragraph in paragraphs]
        return paragraphs

    def compute_paragraph_scores(self):
        paragraphs = self.get_paragraphs(self.article)
        scores = []
        for paragraph in paragraphs:
            scores.append(self.sid.polarity_scores(paragraph)['compound'])
        return scores






