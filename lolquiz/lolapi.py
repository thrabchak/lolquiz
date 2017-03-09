import requests
import tqdm
import json
import datetime
import os.path

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
    return []

  def getChampionAbilities(self, champion):
    '''Returns a list of champion abilities'''
    return []

  def getSummonerSpells(self):
    '''Returns a list of summoner spells'''
    return []

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
      return "-1"

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

class FileSystemService(object):
  """Class used to encapsulate file system calls."""
  DATA_FOLDER_PATH="./data"
  
  def saveJsonFile(self, jsonData, filename):
    with open(self.DATA_FOLDER_PATH + '/' + filename, 'w') as jsonFile:
      json.dump(jsonData, jsonFile)
    return

  def readJsonFile(self, filename):
    filePath = self.DATA_FOLDER_PATH + '/' + filename
    if(os.path.exists(filePath)):
      with open(filePath) as realmFile:
        data = json.load(realmFile)
      return data
    else:
      print("Error: " + filePath + " does not exist.")
      raise Exception
    return ""

  def readFile(self, filename):
    with open(self.DATA_FOLDER_PATH + '/' + filename) as file:
      fileString = file.read().strip()
    return fileString

  def appendFile(self, filename, data):      
    with open(self.DATA_FOLDER_PATH + '/' + filename, 'a') as file:
      file.write(data)
    return

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
