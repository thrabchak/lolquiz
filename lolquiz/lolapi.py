import requests
import json
import datetime

from filesystem import FileSystemService

class LolApi(object):
  """Class containing local lol api functions."""

  '''File name Constants'''
  REALM_FILE='realm.json'
  CHAMPION_FILE="champion.json"
  SUMMONER_SPELL_FILE="summoner_spell.json"

  def __init__(self, fileSystemService=None, apiService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    if(apiService != None):
      self.apiService = apiService
    else:
      self.apiService = RiotApiService(self.fileSystemService)

  def getServerVersion(self):
    '''Returns the api version on data dragon'''
    data = self.apiService.realmRequest()
    return data['dd']

  def getLocalVersion(self):
    '''Returns the api version of the downloaded files'''
    try:
      realmJson = self.fileSystemService.readJsonFile(self.REALM_FILE)
      return realmJson['dd']
    except Exception as e:
      print("Error reading realm file.")
      print(e)
      return "-1"

  def isUpToDate(self):
    '''Returns if the downloaded file versions match the server version'''
    return self.getLocalVersion() == self.getServerVersion()

  def downloadDataFiles(self):
    '''Downloads lol api static data files'''
    self.downloadRealmData()
    self.downloadChampionData()
    self.downloadSummonerSpellData()
    return

  def downloadRealmData(self):
    '''Downloads the realm data'''
    data = self.apiService.realmRequest()
    self.fileSystemService.saveJsonFile(data, self.REALM_FILE)
    return

  def downloadChampionData(self):
    '''Downloads the champion data'''
    data = self.apiService.championRequest()
    self.fileSystemService.saveJsonFile(data, self.CHAMPION_FILE)
    return

  def downloadSummonerSpellData(self):
    '''Downloads the champion data'''
    data = self.apiService.summonerSpellRequest()
    self.fileSystemService.saveJsonFile(data, self.SUMMONER_SPELL_FILE)
    return

  def getChampions(self):
    '''Returns a list of all the active champions'''
    try:
      championJson = self.fileSystemService.readJsonFile(self.CHAMPION_FILE)
      return championJson["data"]
    except Exception as e:
      print("Error reading champion data.")
      return []

  def getItems(self):
    '''Returns a list of all the active items'''
    #TODO
    return []

  def getSummonerSpells(self):
    '''Returns a list of summoner spells'''
    data = self.fileSystemService.readJsonFile(self.SUMMONER_SPELL_FILE)
    spells = []
    for spell in data["data"]:
      if("CLASSIC" in data["data"][spell]["modes"]):
        summonerSpell = SummonerSpell(data["data"][spell])
        spells.append(summonerSpell)
    return spells

class SummonerSpell(object):
  def __init__(self, jsonData):
    self.jsonData = jsonData

  def getCooldown(self):
    return self.jsonData["cooldown"][0]

  def getCooldownString(self):
    cooldown = self.getCooldown()
    mins = int(cooldown // 60)
    secs =  int(cooldown % 60)
    return "{0} mins {1} secs".format(mins, secs) 

  def getName(self):
    return self.jsonData["name"]

class RiotApiService():
  """Class used to encapsulate a https api call to riots static data api endpoint."""
  BASE_API_URL="https://global.api.pvp.net/api/lol/static-data"
  REGION="/na"
  API_VERSION="/v1.2"
  API_KEY_FILE="riot_api_key.txt"
  API_LOG_FILE="api_log.txt"

  def __init__(self, fileSystemService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    self.apiKey = self.getApiKey()

  def getApiKey(self):
    '''Returns the riot api key stored in API_KEY_FILE'''
    try:
      return self.fileSystemService.readFile(self.API_KEY_FILE)
    except Exception as e:
      print("Error reading LoL Api key file.")
      raise e

  def realmRequest(self):
    payload = {"api_key": self.apiKey}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/realm", params=payload)
    self.logApiCall(r)
    data = r.json()
    return data

  def championRequest(self):
    payload = {"api_key": self.apiKey, "champData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/champion", params=payload)
    self.logApiCall(r)
    data = r.json()
    return data

  def summonerSpellRequest(self):
    payload = {"api_key": self.apiKey, "spellData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/summoner-spell", params=payload)
    self.logApiCall(r)
    data = r.json()
    return data

  def logApiCall(self, response):
    '''Logs riot api calls locally in apiLog.txt'''
    time = str(datetime.datetime.now())
    url = str(response.url)
    statusCode = str(response.status_code)

    logString = "{0} : {1} : {2}\n".format(time, statusCode, url)
    self.fileSystemService.appendFile(self.API_LOG_FILE, logString)
    return
