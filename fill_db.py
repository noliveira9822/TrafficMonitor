import pandas as pd
import requests 

TRAFFIC_SPEED_INFO = 'traffic_speed.csv'

traffic_segments = pd.read_csv(TRAFFIC_SPEED_INFO)

api_url = 'http://127.0.0.1:8000/traffic_segment/addsegment'

for row in traffic_segments.itertuples():
    data = {
        "id":row.id,
        "long_start":row.Long_start,
        "lat_start":row.Lat_start,
        "long_end":row.Long_end,
        "lat_end":row.Lat_end,
        "length":row.Length,
        "speed":row.Speed
    }
    response = requests.post(api_url, json=data)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
