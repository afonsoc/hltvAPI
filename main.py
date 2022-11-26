import requests
import json
from bs4 import BeautifulSoup

requestedPage = requests.get("https://www.hltv.org/stats/players")
soup = BeautifulSoup(requestedPage.text, "lxml")

allPlayers = soup.find_all("tr")


playerArray = []

for player in allPlayers:
    if player.find("a") != None:
        playerArray.append({'name': player.find("a").text,
                'link': player.find("a")["href"],
                'stats':{'KD': player.find("td", class_ = "statsDetail").text,
                'Rating': player.find("td", class_ = "ratingCol").text}})

for i in playerArray:
    print(i)
print(len(playerArray))

testname = "OCEAN"

def findByName(playerName):
    playerStats = {}
    relevantStats = ["Total kills", "Headshot %", "Total deaths", "K/D Ratio",
                     "Damage / Round", "Grenade dmg / Round", "Maps played", "Rounds played", "Kills / round",
                     "Assists / round", "Deaths / round", "Saved by teammate / round", "Saved teammates / round",
                     "Rating 2.0"]
    for player in playerArray:
        if player['name'] == playerName:
            playerPage = requests.get("https://www.hltv.org" + player['link'])
            playerSoup = BeautifulSoup(playerPage.text, "lxml")

            allSpans = playerSoup.find_all("span")
            for item in allSpans:
                if item.text in relevantStats:
                    playerStats.update({item.text: item.find_next("span").text})
    return playerStats

print(findByName(testname))

