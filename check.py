import requests

url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=269e2c11b227414faccf57211539c6d6'

# try:
#     response = requests.get(url)
#     response.raise_for_status()
#     data = response.json()
#     print(data["articles"])

# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")

from itertools import product
a = ["A", "B"]
b = ["X", "Y"]
print(product(a,b))