import requests
import json
from datetime import datetime

now = datetime.now()

base_url = f'https://nwis.waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=06043500&legacy=&period=&begin_date=1989-08-01&end_date={now.strftime("%Y-%m-%d")}'

# hourly service:
# https://waterservices.usgs.gov/nwis/iv/?sites=06043500&startDT=2024-06-08T14:19:26.177-06:00&endDT=2024-06-15T14:19:26.177-06:00&parameterCd=00060&format=json

response = requests.get(base_url)
if response.status_code != 200:
    print('You fucked up something. Code: ', response.status_code)

with open(f'data/raw/cfs-daily.txt', 'wb') as f:
    for chunk in response.iter_content(chunk_size=128):
        f.write(chunk)
