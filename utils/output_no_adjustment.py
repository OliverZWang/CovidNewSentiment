from output_scores_and_acc import * 

if __name__ == "__main__":
    ids, gold_labels =  read_labels('../labeled_news/news_labeled.xlsx')
    valid_ids, valid_labels, articles = get_articles_by_id(ids, gold_labels)
    scores_objects = compute_article_sentiment(articles, new_words='None')
    write_article_scores(valid_ids, valid_labels, scores_objects, "../results/no_mod_article_scores.csv")

    accuracy_metrics_dict = compute_opt_accuracy_metrics(scores_objects, valid_labels)
    write_opt_acc_metrics(accuracy_metrics_dict, "../results/no_mod_accuracy_metrics.csv")