# attack.py

import requests
import time

URL = "http://localhost:9000/call-external"

for i in range(20):
    try:
        response = requests.get(URL)
        print(f"{i+1:02d} --> {response.status_code} | {response.json()}")
    except Exception as e:
        print(f"{i+1:02d} --> ERROR: {e}")
    time.sleep(0.5)  # medio segundo entre llamadas