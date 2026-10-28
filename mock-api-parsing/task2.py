import requests
import sys

# class ClientError(Exception):
#     pass

# class ServerError(Exception):
#     pass

# url = "https://jsonplaceholder.typicode.com/invalidroute"

# response = requests.get(url)
# status = response.status_code

# try:
#     if 200 <= status < 300:
#         print(f"Success! Status Code: {status}")

#     elif 400 <= status < 500:
#         print(f"Client Error! Status Code: {status}")
#         raise ClientError(f"HTTP {status} - Client Error")

#     elif 500 <= status < 600:
#         print(f"Server Error! Status Code: {status}")
#         raise ServerError(f"HTTP {status} - Server Error")

#     else:
#         print(f"Unexpected Status Code: {status}")

# except (ClientError, ServerError) as e:
#     print(e)
#     sys.exit(1)

url = "https://jsonplaceholder.typicode.com/posts"
try:
    response = requests.get(url)
    status = response.status_code

    if 200 <= status < 300:
        print("success", status)

    elif 400 <= status < 500:
        print("client error", status)

    elif 500 <= status < 600:
        print("server issues", status)

    else:
        print("unexpected error", status)

except requests.exceptions.RequestException as e:
    print(e)