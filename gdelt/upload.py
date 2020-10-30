import os
import sys
from tqdm import tqdm
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import session, GdeltRaw


files = os.listdir("../data_v1")
# files = ["2020-01-02.json"]
files.sort()

for file in tqdm(files):
    f = open("../data_v1/" + file)
    data = json.load(f)
    f.close()

    i = 0

    for i in tqdm(range(len(data))):
        item = data[i]

        if item['THEMES'] is None:
            continue

        if 'TAX_DISEASE_CORONAVIRUS' not in item['THEMES'] and \
                'WB_2167_PANDEMICS' not in item['THEMES'] and \
                'HEALTH_PANDEMIC' not in item['THEMES']:
            continue

        record_id = "{}-{}".format(item['DATE'], i)

        # if session.query(GdeltRaw).filter(GdeltRaw.record_id == record_id).count() > 0:
        #     continue

        raw = GdeltRaw()

        for key, value in item.items():
            if value is not None and type(value) == str:
                value = value.encode("utf-8")

            setattr(raw, key.lower(), value)

        raw.record_id = record_id

        session.add(raw)

        i += 1

        if i >= 50:
            session.commit()
            i = 0

    session.commit()

    os.rename("../data_v1/" + file, "../data_v1_uploaded/" + file)
