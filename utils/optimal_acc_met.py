
from sentiment_scores import SentimentScores, NEW_WORDS
from accuracy_metrics import AccuracyMetrics
'''

input a list of articles

1. iterate through boundaries
2. create SentimentScores obj for each, store in list
3. compute macro f1 for the specified aggregation methods
4. compute the optimal boundaries

lower starts from -0.75
upper starts from 0.75

return optimal lower, upper boundaries and macro f1


'''
SCORE_TYPES = ['compound_by_article', 'average_sentence', 'median_sentence', 'mode_sentence', 'average_paragraph', 'median_paragraph', 'mode_paragraph']

def compute_article_sentiment(articles):
    scores_objects = []
    for article in articles:
        article_scores = SentimentScores(article)
        scores_objects.append(article_scores)
    return scores_objects

def get_score_by_method(scores_objects, score_type):
    predictions = []
    for scores_object in scores_objects:
        predictions.append(scores_object.result_dict()[score_type])
    return predictions

def find_boundaries(predictions, gold_labels):
    
    opt_lower = -0.75
    opt_upper = 0.75
    max_f1 = 0 

    for lower in range(-0.75, 0.75, 0.05):
        for upper in range(0.75, lower, -0.05):
            metrics = AccuracyMetrics(predictions, gold_labels, neutral_upper=upper, neutral_lower=lower)
            if metrics.macro_f1 > max_f1:
                opt_lower = lower
                opt_upper = upper
                max_f1 = metrics.macro_f1
    
    return opt_lower, opt_upper, metrics

def compute_opt_accuracy_metrics(articles, gold_labels):

    scores_objects = compute_article_sentiment(articles)
    accuracy_metrics_list = []

    for score_type in SCORE_TYPES:
        predictions = get_score_by_method(scores_objects, score_type)
        opt_lower, opt_upper, metrics = find_boundaries(predictions, gold_labels)
        accuracy_metrics_list.append(metrics)



