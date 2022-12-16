import requests
import json
from bs4 import BeautifulSoup

HLTV_PREFIX =  "https://www.hltv.org"

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
    everyPlayerSoup = parsePage("https://www.hltv.org/stats/players").find_all("tr")

    #Get players names and links to overview stats page
    for player in everyPlayerSoup:
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
            return json.dumps(playerStats, indent=2)
    else:
        raise ValueError("Player %s not found" % repr(playerName))

def findTeamByName(teamName):

    #Initiate data structures
    teamStats = {}
    teamArray = []

    #Get parsed teams page
    everyTeamSoup = parsePage("https://www.hltv.org/stats/teams").find_all("tr")

    #Get teams names and links to overview stats page
    for team in everyTeamSoup:
        if team.find("a") != None:
            teamArray.append({'name': team.find("a").text,
                    'link': team.find("a")["href"]})

    for team in teamArray:
        if type(teamName) != str:
            raise AttributeError("Argument %s needs to be a string" % repr(teamName))

        #check if the incoming team request matches value in list
        elif team['name'].upper() == teamName.upper():
            teamSoup = parsePage("https://www.hltv.org" + team['link'])

            #Get list of stats if above check was successful
            allDivs = teamSoup.find_all("div", class_= "large-strong")
            for div in allDivs:
                teamStats.update({div.find_next().text.title().replace(" ", ""): div.text.replace(" ", "")})
            return json.dumps(teamStats, indent=2)
    else:
        raise ValueError("Team %s not found" % repr(teamName))

def findAllPlayers():

    #Get full list of players
    allPlayersSoup = parsePage("https://www.hltv.org/stats/players").find_all("tr")
    playerDict = {}

    #Add values from parsed list to dictionary
    for player in allPlayersSoup:
        if player.find("a") != None:
            playerDict.update({player.find("a")["href"].split("/")[-2]:{"name": player.find("a").text,
            'KD': player.find("td", class_ = "statsDetail").text,
            'Rating': player.find("td", class_ = "ratingCol").text,
            'link': HLTV_PREFIX + player.find("a")["href"]}})

    return json.dumps(playerDict, indent=2)

def findAllTeams():

    #get full list of teams
    allTeamsSoup = parsePage("https://www.hltv.org/stats/teams").find_all("tr")
    teamDict = {}
    
    #Add values from parsed list to dictionary
    for team in allTeamsSoup:
        if team.find("a") != None:
            teamDict.update({team.find("a")["href"].split("/")[-2]:{"name": team.find("a").text,
            'KD': team.find("td", class_ = "statsDetail").text,
            'Rating': team.find("td", class_ = "ratingCol").text,
            'link': HLTV_PREFIX + team.find("a")["href"]}})

    return json.dumps(teamDict, indent=2)