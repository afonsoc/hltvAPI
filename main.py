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
    everyPlayerSoup = parsePage("https://www.hltv.org/stats/players")
    allPlayers = everyPlayerSoup.find_all("tr")

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


testname = "lol"

def findTeamByName(teamName):

    #Initiate data structures
    teamStats = {}
    teamArray = []

    #Get parsed teams page
    everyTeamSoup = parsePage("https://www.hltv.org/stats/teams")
    allTeams = everyTeamSoup.find_all("tr")

    #Get teams names and links to overview stats page
    for team in allTeams:
        if team.find("a") != None:
            teamArray.append({'name': team.find("a").text,
                    'link': team.find("a")["href"]})

    for team in teamArray:
        if type(teamName) != str:
            raise AttributeError("Argument %s needs to be a string" % repr(teamName))

        #check if the incoming team request matches value in list
        elif team['name'].upper() == teamName.upper():
            teamSoup = parsePage("https://www.hltv.org" + team['link'])

    return json.dumps(teamStats, indent=1)

print(findTeamByName(testname))