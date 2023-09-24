import random
import json
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from selenium import webdriver
import redis

HLTV_PREFIX =  "https://www.hltv.org"
USER_AGENT_LIST = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
] 
app = FastAPI()
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/")
async def root():
    return {"test message": "this the the testing message value"}

def parsePage(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument(f'user-agent={random.choice(USER_AGENT_LIST)}')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    requestPage = driver.page_source
    driver.quit()
    return BeautifulSoup(requestPage, "lxml")

@app.get("/players/{playerName}")
async def findPlayerByName(playerName:str):

    #Initiate data structures
    playerStats = {}
    playerArray = []
    relevantStats = ["Total kills", "Headshot %", "Total deaths", "K/D Ratio",
                     "Damage / Round", "Grenade dmg / Round", "Maps played", "Rounds played", "Kills / round",
                     "Assists / round", "Deaths / round", "Saved by teammate / round", "Saved teammates / round",
                     "Rating 1.0"]


    # if cache.get("PLAYERS"):
    #     playersBase = json.loads(cache.get("PLAYERS"))
    #     if playersBase[playerName.upper()]:
    #         return playerName
    #     else:
    #         raise HTTPException(status_code=404, detail="Player %s not found" % repr(playerName))
    # else:
    #Get parsed player page
    everyPlayerSoup = parsePage("https://www.hltv.org/stats/players").find_all("tr")

    #Get players names and links to overview stats page
    for player in everyPlayerSoup:
        if player.find("a") != None:
            playerArray.append({'name': player.find("a").text,
                    'link': player.find("a")["href"]})

    #check if the incoming player request matches value in list
    for player in playerArray:
        if player['name'].upper() == playerName.upper():
            playerSoup = parsePage("https://www.hltv.org" + player['link'])
            
            #Get list of stats if above check was successful
            allSpans = playerSoup.find_all("span")
            for span in allSpans:
                if span.text in relevantStats:
                            playerStats.update({span.text.title().replace(" ", ""): span.find_next("span").text})
            return playerStats
    else:
        raise HTTPException(status_code=404, detail="Player %s not found" % repr(playerName))

@app.get("/teams/{teamName}")
async def findTeamByName(teamName:str):

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

        #check if the incoming team request matches value in list
    for team in teamArray:
        if team['name'].upper() == teamName.upper():
            teamSoup = parsePage("https://www.hltv.org" + team['link'])

            #Get list of stats if above check was successful
            allDivs = teamSoup.find_all("div", class_= "large-strong")
            for div in allDivs:
                teamStats.update({div.find_next().text.title().replace(" ", ""): div.text.replace(" ", "")})
            return teamStats
    else:
        raise HTTPException(status_code=404, detail="Team %s not found" % repr(teamName))

@app.get("/players")
async def findAllPlayers():

    #Get full list of players
    playerDict = {}

    if cache.get("PLAYERS"):
        # for player in teams_cache:
        #     cacheValue = teams_cache[player]
        #     for key in cacheValue:
        #         playerDict.update({key: cacheValue[key]})
        return json.loads(cache.get("PLAYERS"))
    else:
        #Add values from parsed list to dictionary
        allPlayersSoup = parsePage("https://www.hltv.org/stats/players").find_all("tr")
        for player in allPlayersSoup:
            if player.find("a") != None:
                playerDict.update({ player.find("a").text.upper():{
                    'KD': player.find("td", class_ = "statsDetail").text,
                    'Rating': player.find("td", class_ = "ratingCol").text,
                    'link': HLTV_PREFIX + player.find("a")["href"]
                }})
        cache.set("PLAYERS", json.dumps(playerDict))
        return playerDict
        


@app.get("/teams")
async def findAllTeams():

    #get full list of teams
    teamDict = {}

    if cache.get("TEAMS"):
        # for team in json.loads(cache.get("TEAMS")):
        #     cacheValue = json.loads(cache.get(team))
        #     for key in cacheValue:
        #         teamDict.update({key: cacheValue[key]})
        return json.loads(cache.get("TEAMS"))
    else:
        #Add values from parsed list to dictionary
        allTeamsSoup = parsePage("https://www.hltv.org/stats/teams").find_all("tr")
        for team in allTeamsSoup:
            if team.find("a") != None:
                teamDict.update({team.find("a").text.upper():{
                    'KD': team.find("td", class_ = "statsDetail").text,
                    'Rating': team.find("td", class_ = "ratingCol").text,
                    'link': HLTV_PREFIX + team.find("a")["href"]
                }})
        cache.set("TEAMS", json.dumps(teamDict))
        return teamDict