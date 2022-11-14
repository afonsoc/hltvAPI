import requests
import json
from bs4 import BeautifulSoup

requestedPage = requests.get("https://www.hltv.org/stats/players")
soup = BeautifulSoup(requestedPage.text, "lxml")

allPlayers = soup.find_all("tr")


playerArray = []

for player in allPlayers:
    if player.find("a") != None:
        playerArray.append(json.dumps({'Name': player.find("a").text,
                'stats':{'KD': player.find("td", class_ = "statsDetail").text, 
                'Rating': player.find("td", class_ = "ratingCol").text}}, indent = 2))

for i in playerArray:
    print(i)
print(len(playerArray))