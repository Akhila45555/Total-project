# import requests
# URL = "https://jsonplaceholder.typicode.com/posts"
# try:
#     response = requests.get(URL)
#     print(response.status_code)
# except requests.exceptions.RequestException as e:
#     print("Error:", e)

# import requests
# URL = "https://jsonplaceholder.typicode.com/posts"
# try:
#     response = requests.get(URL)
#     print(response)
# except requests.exceptions.RequestException as e:
#     print("error", e)

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
try:
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
      data = response.json()
    print("ID:", data["id"])
    print("TITLE:", data["title"])

except requests.exceptions.RequestException as e:
 print("Error:", e)