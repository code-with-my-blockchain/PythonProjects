import requests
import json

query = input("What type of news are you interested in? ")

url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey=59d57c9ab56e40d494dd35b60acdbcd8"

try:
    r = requests.get(url)
    r.raise_for_status
    news = json.loads(r.text)

    for article in news["articles"]:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print("--------------------------------------")
except requests.exceptions.ConnectionError:
    print("Internet ")
except Exception as e:
   print(f": {e}")   
   