import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import gdelt
from datetime import date, timedelta
from tqdm import tqdm


def download_data(start: date, end: date):
    gd = gdelt.gdelt(version=1)

    delta = end - start

    for i in tqdm(range(delta.days + 1)):
        day = start + timedelta(days=i)
        day_str = str(day)

        try:
            results = gd.Search(day_str, table='gkg', output='json')
        except ValueError:
            continue

        f = open("../data_v1/{}.json".format(day_str), "w")
        f.write(results)
        f.close()


if __name__ == '__main__':
    download_data(date(2020, 1, 1), date(2020, 1, 31))
