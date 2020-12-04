from output_scores_and_acc import * 
import pymysql.cursors

def get_gdelt_scores(valid_ids):
    connection = pymysql.connect(host="nlp2590.ckdech7dwvqp.us-east-1.rds.amazonaws.com",
    port=3310,
    user='nlp2590',
    password='lDABt9PoT7wJcdjljome',
    db='nlp2590')
    
    scores = []
    try:
        with connection.cursor() as cursor:

            for id in valid_ids:
                sql = f'select TONE from `gdelt_raw` where RECORDID = "{id}"; '
                cursor.execute(sql)
                row = cursor.fetchone()
                score = float(row[0].split(',')[0])
                scores.append(score)
    finally:
        connection.close()
    return scores

def write_gdelt_scores(valid_ids, gdelt_scores, valid_labels):
    with open('../results/gdelt_scores.csv', mode='w') as csv_file:
        score_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        score_writer.writerow(['RECORDID', 'gdelt_score', 'gold_labels'])

        for itr in range(len(valid_ids)):
            score_writer.writerow([valid_ids[itr], str(gdelt_scores[itr]), str(valid_labels[itr])])

def write_gdelt_acc_metrics(gdelt_scores, valid_labels):
    opt_metrics = find_opt_metrics(gdelt_scores, valid_labels, lower_bound=-10, upper_bound=10, step=0.2)
    with open('../results/gdelt_acc_metrics.csv', mode='w') as csv_file:
        accuracy_writer = csv.writer(csv_file, delimiter=",", quotechar='"')
        accuracy_writer.writerow(['method'] + list(opt_metrics.result_dict().keys()) + ['neutral_lower', 'neutral_upper'])
        accuracy_writer.writerow(['gdelt_sent_score'] + list(opt_metrics.result_dict().values()) + [str(opt_metrics.neutral_lower), str(opt_metrics.neutral_upper)])


if __name__ == "__main__":
    ids, gold_labels =  read_labels('../labeled_news/news_labeled.xlsx')
    valid_ids, valid_labels, articles = get_articles_by_id(ids, gold_labels)
    gdelt_scores = get_gdelt_scores(valid_ids)
    # write_gdelt_scores(valid_ids, gdelt_scores, valid_labels)
    write_gdelt_acc_metrics(gdelt_scores, valid_labels)