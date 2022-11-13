import requests
import json
from bs4 import BeautifulSoup

requestedPage = requests.get("https://www.hltv.org/stats/players")
soup = BeautifulSoup(requestedPage.text, "lxml")

allPlayers = soup.find_all("tr")


playerArray = []

for player in allPlayers:
    # testvar = player.text
    if player.find("a") != None:
        playerArray.append({'Name': player.find("a").text,
                'KD': player.find("td", class_ = "statsDetail").text, 
                'Rating': player.find("td", class_ = "ratingCol").text})
    

# print(len(playerArray))
# print(player.text)

print(type(playerArray[-1]))

for i in playerArray:
    print(i)
print(len(playerArray))
print(type(playerArray[-1]))

test = json.dumps(playerArray[-1])

print(type(test))
        