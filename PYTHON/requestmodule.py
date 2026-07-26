import requests 

# GET Request Example
# response = requests.get("https://www.google.com")
# print(response.text)

# POST Request Example
url = "https://jsonplaceholder.typicode.com/posts"
data = {
    "title": 'harry',
    "body": 'bhai',
    "userId": 12,
}
headers =  {
    'Content-type': 'application/json; charset=UTF-8',
  }
response = requests.post(url, headers=headers, json=data)

print(response.text)