import requests
import json
from datetime import datetime

start_year = 1990
end_hour = '23:00'
now = datetime.now()
current_year = now.year
current_hour = now.hour

date_tuples = []
for year in range(start_year, current_year + 1):
    start_date = f'{year}-01-01 00:00'
    if year == current_year:
        end_date = now.strftime('%Y-%m-%d %H:00')
    else:
        end_date = f'{year}-12-31 {end_hour}'
    date_tuples.append((start_date, end_date))

base_url = 'https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data'
for dt in date_tuples:
    print(f'Fetching hourly for {dt[0]} to {dt[1]}')
    params = {
            'stationTriplets': '754:MT:SNTL',
            'elements': 'WTEQ,TOBS',
            'duration': 'HOURLY',
            'beginDate': dt[0],
            'endDate': dt[1],
            'periodRef': 'END',
            'centralTendencyType': 'AVERAGE',
            'returnFlags': 'true',
            'returnOriginalValues': 'true',
            'returnSuspectData': 'true'
            }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print('You fucked up something. Code: ', response.status_code)
        print('Params: ', params)

    with open(f'data/raw/sntl-{dt[0]}.json', 'w') as f:
        json.dump(response.json(), f, indent=4)
