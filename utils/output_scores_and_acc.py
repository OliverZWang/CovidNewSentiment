
from sentiment_scores import SentimentScores, NEW_WORDS
from accuracy_metrics import AccuracyMetrics
import pandas as pd
import pymysql.cursors
import csv
import numpy as np


SCORE_TYPES = ['compound_by_article', 'average_sentence', 'median_sentence', 'mode_sentence', 'average_paragraph', 'median_paragraph', 'mode_paragraph', 'avg_first_last_para']

'''
    Input: a list of articles
    Output: a list of SentimentScores objects for the input articles
'''
def compute_article_sentiment(articles, new_words='default', method='default'):
    scores_objects = []
    for article in articles:
        article_scores = SentimentScores(article, new_words=new_words, method=method)
        scores_objects.append(article_scores)
    return scores_objects

'''
    Input: a list of SentimentScores objects; method to calculate score
    Output: a list of sentiment scores calculated based on the specified by input
'''
def get_score_by_method(scores_objects, score_type):
    predictions = []
    for scores_object in scores_objects:
        predictions.append(scores_object.result_dict()[score_type])
    return predictions

'''
    Input: a list of sentiment scores; a list of gold labels
    Output: a AccuracyMetrics object using the optimal boundaries

'''
def find_opt_metrics(predictions, gold_labels, lower_bound=-1, upper_bound=1, step=0.05):
    
    # opt_lower = -0.75
    # opt_upper = 0.75
    max_f1 = 0 
    opt_metrics = None
    for lower in np.arange(lower_bound, upper_bound, step):
        for upper in np.arange(upper_bound, lower, step*-1):
            metrics = AccuracyMetrics(predictions, gold_labels, neutral_upper=upper, neutral_lower=lower)
            if metrics.macro_f1 > max_f1:
                # opt_lower = lower
                # opt_upper = upper
                max_f1 = metrics.macro_f1
                opt_metrics = metrics
    
    return opt_metrics

'''
    Input: A list of SentimentScores objects; a list of gold labels
    Output: A dictionary that maps each aggregation method to its AccurarcyMetrics object
'''
def compute_opt_accuracy_metrics(scores_objects, gold_labels):

    # scores_objects = compute_article_sentiment(articles)
    accuracy_metrics_dict = {}

    for score_type in SCORE_TYPES:
        predictions = get_score_by_method(scores_objects, score_type)
        metrics = find_opt_metrics(predictions, gold_labels)
        accuracy_metrics_dict[score_type] = metrics

    return accuracy_metrics_dict


'''
    Input: the path to the excel file containing article IDs and labels
    Output: a list of RECORDIDs; a list of gold labels
'''
def read_labels(filename):

    excel_file = pd.read_excel(filename)
    # print(excel_file.head())

    ids = excel_file.iloc[:, 1].tolist()
    gold_labels = excel_file.iloc[:, 2].tolist()

    return ids, gold_labels
    

'''
    Input: a list of RECORDIDs, a list of gold labels
    Output: a list of labels, and a list of gold labels for articles that have valid bodies; a list of articles
'''
def get_articles_by_id(ids, gold_labels):

    connection = pymysql.connect(host="nlp2590.ckdech7dwvqp.us-east-1.rds.amazonaws.com",
    port=3310,
    user='nlp2590',
    password='lDABt9PoT7wJcdjljome',
    db='nlp2590')
    
    valid_ids = []
    valid_labels = []
    articles = []

    try:
        with connection.cursor() as cursor:

            for index in range(len(ids)):
                sql = f'select * from `news` where RECORDID = "{ids[index]}" ' 
                cursor.execute(sql)
                rows = cursor.fetchone()
                if rows[3] != '':
                    valid_ids.append(ids[index])
                    valid_labels.append(gold_labels[index])
                    articles.append(rows[3])
    finally:
        connection.close()

    return valid_ids, valid_labels, articles

def write_article_scores(valid_ids, gold_labels, scores_objects, path):

    with open(path, mode="w") as csv_file:

        score_writer = csv.writer(csv_file, delimiter=",", quotechar='"')
        score_writer.writerow(['RECORDID', 'gold_labels']+ list(scores_objects[0].result_dict().keys()))

        for itr in range(len(scores_objects)):
            score_writer.writerow([valid_ids[itr], str(gold_labels[itr])] + list(scores_objects[itr].result_dict().values()))

def write_opt_acc_metrics(accuracy_metrics_dict, path):

    with open(path, mode='w') as csv_file:
        accuracy_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        accuracy_writer.writerow(['aggregation_method'] + list(accuracy_metrics_dict['compound_by_article'].result_dict().keys()) + ['neutral_lower', 'neutral_upper'])

        for key in accuracy_metrics_dict.keys():
            this_met = accuracy_metrics_dict[key]
            accuracy_writer.writerow([key] + list(this_met.result_dict().values()) + [str(this_met.neutral_lower), str(this_met.neutral_upper)])

if __name__ == "__main__":
    
    ids, gold_labels =  read_labels('../labeled_news/news_labeled.xlsx')
    valid_ids, valid_labels, articles = get_articles_by_id(ids, gold_labels)
    scores_objects = compute_article_sentiment(articles)

    write_article_scores(valid_ids, valid_labels, scores_objects, "../results/article_scores.csv")

    accuracy_metrics_dict = compute_opt_accuracy_metrics(scores_objects, valid_labels)
    write_opt_acc_metrics(accuracy_metrics_dict, "../results/accuracy_metrics.csv")

    # print(accuracy_metrics_dict['average_sentence'].neutral_lower, accuracy_metrics_dict['average_sentence'].neutral_upper)
