import pandas as pd
import pymysql.cursors
from output_scores_and_acc import compute_article_sentiment, get_score_by_method
import datetime
import time


def convert_date(date_as_int):
    date_as_str = str(date_as_int)
    return datetime.date(int(date_as_str[0:4]), int(date_as_str[4:6]), int(date_as_str[6:8]))

def get_all_valid_articles():
    connection = pymysql.connect(host="nlp2590.ckdech7dwvqp.us-east-1.rds.amazonaws.com",
    port=3310,
    user='nlp2590',
    password='lDABt9PoT7wJcdjljome',
    db='nlp2590')
    
    valid_ids = []
    articles = []
    dates = []

    try: 
        with connection.cursor() as cursor:
            sql = 'select news.RECORDID, news.body, gdelt_raw.DATE from news inner join gdelt_raw on news.RECORDID = gdelt_raw.RECORDID where news.body != ""; '
            print('starting database request')
            cursor.execute(sql)
            print('executed sql command')
            rows = cursor.fetchall()
            print('fetched data')
            for row in rows:
                valid_ids.append(row[0])
                articles.append(row[1])
                dates.append(convert_date(row[2]))
            print('finished reading data')
    finally:
        connection.close()
    return valid_ids, articles, dates

def map_predictions(predictions, neutral_lower, neutral_upper):
    print('starting to map predictions')
    mapped_predictions = []
    for index in range(len(predictions)):
        if predictions[index] <= neutral_lower:
            mapped_predictions.append(-1)
        elif predictions[index] <= neutral_upper:
            mapped_predictions.append(0)
        else:
            mapped_predictions.append(1)
    print('finished mapping predictions')
    return mapped_predictions

def execute_sql(sql):
    connection = pymysql.connect(host="nlp2590.ckdech7dwvqp.us-east-1.rds.amazonaws.com",
    port=3310,
    user='nlp2590',
    password='lDABt9PoT7wJcdjljome',
    db='nlp2590')

    try: 
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
        connection.commit()
    finally:
        connection.close()

def upload_time_series(valid_ids, dates, sentiment_scores, predictions):
    connection = pymysql.connect(host="nlp2590.ckdech7dwvqp.us-east-1.rds.amazonaws.com",
    port=3310,
    user='nlp2590',
    password='lDABt9PoT7wJcdjljome',
    db='nlp2590')

    try:
        with connection.cursor() as cursor:
            
            print('starting to upload results')
            for index in range(len(valid_ids)):
                # print(dates[index])
                sql = f'insert into `vader_time_series`  VALUES({valid_ids[index]}, "{dates[index]}", {sentiment_scores[index]}, {predictions[index]});'
                # print(sql)
                cursor.execute(sql)
            print('finished uploading results')
        connection.commit()

    finally:
        connection.close()

def write_to_csv(valid_ids, dates, sentiment_scores, predictions, path):
    print('starting to write csv')
    col_dict = {'RECORDID': valid_ids, 'dates': dates, 'sentiment_scores': sentiment_scores, 'predictions': predictions}
    df = pd.DataFrame(col_dict)
    df.to_csv(path, mode='a', index=False, header=False)
    print('finished writing csv')

def get_paragraph_average(scores_objects):
    sentiment_scores = []
    for obj in scores_objects:
        sentiment_scores.append(obj.average_paragraph)
    return sentiment_scores

def split_to_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i+n]

if __name__ == "__main__":
    
    valid_ids, articles, dates = get_all_valid_articles()
    # print('starting to score articles')
    # start_time = time.time()
    program_start = time.time()
    drop_if_exists_sql = 'drop table if exists vader_time_series; '
    create_table_sql = 'create table vader_time_series(RECORDID INt, DATE DATE, sentiment_scores FLOAT, predictions INT);'


    execute_sql(drop_if_exists_sql)
    execute_sql(create_table_sql)

    valid_ids_chunks = list(split_to_chunks(valid_ids, 1000))
    articles_chunks = list(split_to_chunks(articles, 1000))
    dates_chunks = list(split_to_chunks(dates, 1000))

    for chunk_index in range(len(valid_ids_chunks)):

        print(f'Starting chunk {chunk_index}/{len(valid_ids_chunks)}. ')
        valid_ids = valid_ids_chunks[chunk_index]
        articles = articles_chunks[chunk_index]
        dates = dates_chunks[chunk_index]

        start_time = time.time()
        scores_objects = compute_article_sentiment(articles, new_words='default', method='average_paragraph')
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print('finished scoring articles')


    
        sentiment_scores = get_paragraph_average(scores_objects)
        predictions = map_predictions(sentiment_scores, 0, 0.15)

        upload_time_series(valid_ids, dates, sentiment_scores, predictions)
        write_to_csv(valid_ids, dates, sentiment_scores, predictions, '../results/all_article_vader.csv')

        print(f'Finished chunk {chunk_index}/{len(valid_ids_chunks)}. Time: {time.time() - start_time}')

    print(f'Total time: {time.time() - program_start}')
    # print(sentiment_scores)
    # print(predictions)

    # execute_sql('drop table labelled_news')
# my_inst = 1
# my_tuple = (my_inst, 2)
# print(my_tuple)
# df = pd.DataFrame(columns=['col1', 'col2', 'col3'])
# df = df.append(pd.Series([1, '2', 3.0], index=df.columns), ignore_index=True)
# print(df)
    # print(dates)
    # print(datetime.date(2020, 2, 4))


        


    # print("--- %s seconds ---" % (time.time() - start_time))