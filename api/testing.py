from urllib import response
import requests
from random import randint

URL = "http://127.0.0.1:8000/"

# response = requests.get(URL + "todo/")
# response = requests.post(URL + "todo/", data={"title": f"test{randint(1, 100)}"})
# response = requests.put(URL + "todo/", data={"id": 2, "title": "updated Title", 'done': True})
response = requests.delete(URL + "todo/", data={"id": 2})
# print(response.json())
print(response.text)