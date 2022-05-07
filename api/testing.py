from urllib import response
import requests
from random import randint

URL = "http://127.0.0.1:8000/"


# none of these will work anymore because the api is now listening for application/json not application/x-www-form-urlencoded which is what python sends


# response = requests.get(URL + "todo/")
response = requests.post(URL + "todo/", data={"title": f"test{randint(1, 100)}"})
# response = requests.put(URL + "todo/", data={"id": 2, "title": "updated Title", 'done': True})
# response = requests.delete(URL + "todo/", data={"id": 2})
# print(response.json())


# response = requests.post(URL + "todo/")


response = requests.options(URL)

print(response.text)
print(response.status_code)