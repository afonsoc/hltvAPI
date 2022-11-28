import requests
import json
from bs4 import BeautifulSoup

def parsePage(url):
    return BeautifulSoup(requests.get(url).text, "lxml")

def findPlayerByName(playerName):

    #Initiate data structures
    playerStats = {}
    playerArray = []
    relevantStats = ["Total kills", "Headshot %", "Total deaths", "K/D Ratio",
                     "Damage / Round", "Grenade dmg / Round", "Maps played", "Rounds played", "Kills / round",
                     "Assists / round", "Deaths / round", "Saved by teammate / round", "Saved teammates / round",
                     "Rating 1.0"]

    #Get parsed player page
    EveryPlayerSoup = parsePage("https://www.hltv.org/stats/players")
    allPlayers = EveryPlayerSoup.find_all("tr")

    #Get players names and links to overview stats page
    for player in allPlayers:
        if player.find("a") != None:
            playerArray.append({'name': player.find("a").text,
                    'link': player.find("a")["href"]})


    for player in playerArray:
        if type(playerName) != str:
            raise AttributeError("Argument %s needs to be a string" % repr(playerName))

        #check if the incoming player request matches value in list
        elif player['name'].upper() == playerName.upper():
            playerSoup = parsePage("https://www.hltv.org" + player['link'])
            
            #Get list of stats if above check was successful
            allSpans = playerSoup.find_all("span")
            for span in allSpans:
                if span.text in relevantStats:
                            playerStats.update({span.text.title().replace(" ", ""): span.find_next("span").text})
            return json.dumps(playerStats, indent=1)
    else:
        raise ValueError("Player %s not found" % repr(playerName))

