# import requests
# url= "https://jsonplaceholder.typicode.com/posts/1"
# response = requests.get(url)
# payload = response.json()
# title = payload.get("title", "Default Token")
# body = payload.get("body", "No Body")
# title = title.strip()
# body = body.strip()
# print("Title:", title)
# print("Body:", body)
# print("Title Length:", len(title))
# print("Body Length:", len(body))

import requests
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
data = response.json()
title = data.get("title", "").strip()
body = data.get("body", "").strip()
print("Title:", title)
print("Body:", body)
print("Title Length:", len(title))
print("Body Length:", len(body))