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
    start_date = f'{year}-01-01T00:00'
    if year == current_year:
        end_date = now.strftime('%Y-%m-%dT%H:00')
    else:
        end_date = f'{year}-12-31T{end_hour}'
    date_tuples.append((start_date, end_date))
print(date_tuples)

base_url = 'https://waterservices.usgs.gov/nwis/iv/'

# hourly service:
# https://waterservices.usgs.gov/nwis/iv/?sites=06043500&startDT=2024-06-08T14:19:26.177-06:00&endDT=2024-06-15T14:19:26.177-06:00&parameterCd=00060&format=json
for dt in date_tuples:
    print(f'Fetching hourly for {dt[0]} to {dt[1]}')
    params = {
            'sites': '06043500',
            'startDT': dt[0],
            'endDT': dt[1],
            'parameterCd': '00060',
            'format': 'json'
            }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print('You fucked up something. Code: ', response.status_code)
        print('Params: ', params)

    with open(f'data/raw/cfs-{dt[0]}.json', 'w') as f:
        json.dump(response.json(), f, indent=4)
