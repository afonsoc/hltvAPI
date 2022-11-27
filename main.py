import requests
import json
from bs4 import BeautifulSoup

def parsePage(url):
    return BeautifulSoup(requests.get(url).text, "lxml")

soup = parsePage("https://www.hltv.org/stats/players")

allPlayers = soup.find_all("tr")


playerArray = []

for player in allPlayers:
    if player.find("a") != None:
        playerArray.append({'name': player.find("a").text,
                'link': player.find("a")["href"]})

for i in playerArray:
    print(i)
print(len(playerArray))

testname = "ocean"

def findByName(playerName):
    playerStats = {}
    relevantStats = ["Total kills", "Headshot %", "Total deaths", "K/D Ratio",
                     "Damage / Round", "Grenade dmg / Round", "Maps played", "Rounds played", "Kills / round",
                     "Assists / round", "Deaths / round", "Saved by teammate / round", "Saved teammates / round",
                     "Rating 1.0"]

    for player in playerArray:
        if player['name'].upper() == playerName.upper():
            playerSoup = parsePage("https://www.hltv.org" + player['link'])

            allSpans = playerSoup.find_all("span")
            for span in allSpans:
                if span.text in relevantStats:
                            playerStats.update({span.text.title().replace(" ", ""): span.find_next("span").text})
            return json.dumps(playerStats, indent=1)

print(findByName(testname))

