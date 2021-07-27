# Test reading the API responses 

import requests

url = "http://127.0.0.1:5000//api/v1.0/2016-08-26/2016-09-01"
test = requests.get(url).json()
print(f"Test url = {url}")
print(f"Result = {test}")

url = "http://127.0.0.1:5000//api/v1.0/2016-08-26"
test = requests.get(url).json()
print(f"Test url = {url}")
print(f"Result = {test}")

url = "http://127.0.0.1:5000//api/v1.0/tobs"
test = requests.get(url).json()
print(f"Test url = {url}")
print(f"Station meta data = {test[0]}")
for t in test[1]:
    print(f"Observation = {t}")

url = "http://127.0.0.1:5000//api/v1.0/station"
test = requests.get(url).json()
print(f"Test url = {url}")
for t in test:
    print(t)

url = "http://127.0.0.1:5000//api/v1.0/precipitation"
test = requests.get(url).json()
print(f"Test url = {url}")
print(f"Station meta data = {test[0]}")
for t in test[1]:
    print(f"Observation = {t}")

