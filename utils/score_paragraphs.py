from output_scores_and_acc import read_labels, get_articles_by_id, compute_article_sentiment
import json

if __name__ == "__main__":
    ids, gold_labels =  read_labels('../labeled_news/news_labeled.xlsx')
    valid_ids, valid_labels, articles = get_articles_by_id(ids, gold_labels)
    scores_objects = compute_article_sentiment(articles)
    
    output = []

    for obj in scores_objects: 
        paragraphs = obj.get_paragraphs(obj.article)
        for index in range(len(obj.scores_by_paragraph)):
            if obj.scores_by_paragraph[index] != 0:
                if obj.scores_by_paragraph[index] >= 0:
                    output.append({paragraphs[index]: 1})
                else:
                    output.append({paragraphs[index]: -1})
    with open('../results/paragraph_scores_binary.json', 'w') as outfile:
        json.dump(output, outfile)

