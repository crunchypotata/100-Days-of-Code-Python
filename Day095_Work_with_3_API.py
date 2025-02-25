import os
import requests
import json
import openai
from requests.auth import HTTPBasicAuth

max = 10
news = os.environ["news"]
openai.organisation = os.environ["organisationID"]
openai.api_key = os.environ["openai"]
openai.Model.list()

country = "gb"
url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey{news}"

result = requests.get(url)
data = result.json()
# print(json.dumps(data, intent=2))

responses =[]
counter = 0 
for article in data["articles"]:
    counter +=1 
    if counter > max:
        break
    prompt = (f"""Summarise{article["url"]} no more than 5 words""")
    response = openai.Completition.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=20)
    # print(response["choises"][0]["text"].strip())
    responses.append(response["choises"][0]["text"].strip())


    time.sleep(20) #fix error

clientID = os.environ['CLIENT_ID']
clientSECRET = os.environ['CLIENT_SECRET']

url = "https://accounts.spotify.com/api/token"
data = { "grant_type": "client_credentials"}
auth = HTTPBasicAuth(clientID, clientSECRET)

response = requests.post(url, data=data, auth=auth)
accessToken = response.json()["access_token"]
headers = {"Authorization" : f"Bearer{accessToken}"}

songs = []

for response in responses:
    headline = response.replace(" ", "%20")
    headline = response.replace(".", "")
    url = "https://api.spotify.com/v1/search"
    search = f"?q={headline}&type=track"
    fullURL = f"{url}{search}"
    # print(fullURL)
    response = requests.get(fullURL, headers=headers)
    data = response.json()
    try:    
        songs.append(data["tracks"]["items"][0])
    except:
        songs.append({"name" : None, "preview_url" : None})

for i in range(max):
    if songs[i]["name"] != None:
        print(responses[i])
        print(songs[i]["name"])
        print(songs[i]["preview_url"])
        print()