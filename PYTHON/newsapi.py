import requests
import json

query = input("What type of news are you interested in? ")
api_key = "59d57c9ab56e40d494dd35b60acdbcd8" 
url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"

r = requests.get(url)
news = json.loads(r.text)

if news.get("status") == "ok":
    for article in news["articles"]:
        print(article["title"])
        print(article["description"])
        print("--------------------------------------")
else:
    print("Error:", news.get("message", "Unknown Error occurred"))