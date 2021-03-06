import requests
import json
import datetime

from filesystem import FileSystemService

class LolApi(object):
  """Class containing local lol api functions."""

  '''File name Constants'''
  REALM_FILE='realm.json'
  CHAMPION_FILE="champion.json"
  SUMMONER_SPELL_FILE="summoner.json"
  ITEM_FILE="items.json"

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
      if(not self.fileSystemService.exists(self.REALM_FILE)):
        return -1
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
    self.downloadItemData()
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

    for champ in self.getChampions():
      data = self.apiService.specificChampionRequest(champ.jsonData['id'])
      self.fileSystemService.saveJsonFile(data, champ.jsonData['id']+".json")
    return

  def downloadSummonerSpellData(self):
    '''Downloads the champion data'''
    data = self.apiService.summonerSpellRequest()
    self.fileSystemService.saveJsonFile(data, self.SUMMONER_SPELL_FILE)
    return

  def downloadItemData(self):
    '''Downloads the item data'''
    data = self.apiService.itemRequest()
    self.fileSystemService.saveJsonFile(data, self.ITEM_FILE)
    return

  def getChampions(self):
    '''Returns a list of all the active champions'''
    try:
      championJson = self.fileSystemService.readJsonFile(self.CHAMPION_FILE)
      champs = []
      for champKey, champValue in championJson["data"].items():
        champs.append(Champion(champValue))
      return champs
    except Exception as e:
      print("Error reading champion data.")
      print(e)
      raise e
    return []

  def getChampion(self, id):
    '''Returns the champion'''
    try:
      championJson = self.fileSystemService.readJsonFile(id + ".json")
      for champKey, champValue in championJson["data"].items():
        return Champion(champValue)
    except Exception as e:
      print("Error reading champion data.")
      print(e)
      raise e
    return None

  def getItems(self):
    '''Returns a list of all the active items'''
    excludedItems = frozenset([
      3635 # Port pad
      ])
    try:
      itemJson = self.fileSystemService.readJsonFile(self.ITEM_FILE)
      items = []
      for itemKey, itemValue in itemJson["data"].items():
        isOnSummonersRift = itemValue["maps"]["11"]
        isPurchasable = itemValue["gold"]["purchasable"]
        isExcluded = (int(itemKey) in excludedItems)
        isInStore = True
        if("inStore" in itemValue.keys()):
          isInStore = itemValue["inStore"]
        if(isOnSummonersRift and isPurchasable and isInStore and not isExcluded):
          items.append(Item(itemValue))
      return items
    except Exception as e:
      print("Error reading item data.")
      print(e)
      raise e
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

class Champion(object):

  def __init__(self, jsonData):
    self.jsonData = jsonData

  def getAbilities(self):
    '''Get list of champion's abilities (includes passive)'''
    abilities = []
    passive = Ability(self.jsonData["passive"])
    abilities.append(passive)
    for spell in self.jsonData["spells"]:
        abilities.append(Ability(spell))
    return abilities

  def getAbilitiesAsStrings(self):
    abilities = self.getAbilities()
    stringList = []
    for ability in abilities:
      abilityString = r"{0}{1}\n{2}".format(ability.getName(), ability.getCooldownString(), ability.description())
      stringList.append(abilityString)
    return stringList

  def getAbilitiesAsHtml(self):
    abilities = self.getAbilities()
    stringList = []
    for ability in abilities:
      abilityString = "{0}{1}<br>{2}".format(ability.getName(), ability.getCooldownString(isHtml=True), ability.description())
      stringList.append(abilityString)
    return stringList

  def getStats(self):
    return self.jsonData["stats"]

  def getAllyTips(self):
    '''Returns a list of strings containing helpful advice'''
    return self.jsonData["allytips"]

  def getEnemyTips(self):
    '''Returns a list of strings containing cautionary advice'''
    return self.jsonData["enemytips"]

  def getName(self):
    return self.jsonData["name"]

class Ability():

  def __init__(self, jsonData):
    self.jsonData = jsonData

  def getName(self):
    return self.jsonData["name"]

  def description(self):
    return str(self.jsonData["description"])

  def getCooldownString(self, isHtml=False):

    if("cooldown" not in self.jsonData.keys()):
      return ""

    cooldownList = self.jsonData["cooldown"] 

    if(isHtml):
      prefix = "<br>Cooldown: "
    else:
      prefix = "\nCooldown: "

    allTheSame = True
    for i in cooldownList:
      if(i != cooldownList[0]):
        allTheSame = False

    if(allTheSame):
      return prefix + str(cooldownList[0])

    stringList = []
    for i in cooldownList:
      stringList.append(str(i))
      stringList.append("/")
    stringList.pop()
    return prefix + "".join(stringList)

class Item(object):

  def __init__(self, jsonData):
    self.jsonData = jsonData

  def getName(self):
    return str(self.jsonData["name"])

  def description(self):
    return r"{0}\n\nCost: {1}".format(self.jsonData["sanitizedDescription"], self.getCost())

  def html(self):
    return r"{0}<br><br>Cost: {1}".format(self.jsonData["description"], self.getCost())

  def getCost(self):
    return self.jsonData["gold"]["total"]

class RiotApiService():
  """Class used to encapsulate a https api call to riots static data api endpoint."""
  BASE_API_URL="https://ddragon.leagueoflegends.com"
  REGION=""
  API_VERSION="/cdn/11.5.1/data/en_US"
  API_KEY_FILE="riot_api_key.txt"
  API_KEY_ENV="RIOT_API_KEY"
  API_LOG_FILE="api_log.txt"

  def __init__(self, fileSystemService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    self.apiKey = ""

  def getApiKey(self):
    '''Returns the riot api key stored in API_KEY_FILE'''
    try:
      return self.apiKey#self.fileSystemService.getEnv(self.API_KEY_ENV)
    except Exception as e:
      print("Error reading RIOT_API_KEY env.")
      raise e

  def realmRequest(self):
    payload = {"api_key": self.apiKey}
    r = requests.get(self.BASE_API_URL + "/realms/na.json")
    self.logApiCall(r)
    data = r.json()

    return data

  def championRequest(self):
    payload = {"api_key": self.apiKey, "champData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/champion.json")
    self.logApiCall(r)
    data = r.json()
    return data

  def specificChampionRequest(self, id):
    payload = {"api_key": self.apiKey, "champData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/champion/" + id + ".json")
    self.logApiCall(r)
    data = r.json()
    return data

  def summonerSpellRequest(self):
    payload = {"api_key": self.apiKey, "spellData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/summoner.json")
    self.logApiCall(r)
    data = r.json()
    return data

  def itemRequest(self):
    payload = {"api_key": self.apiKey, "itemListData": "all"}
    r = requests.get(self.BASE_API_URL + self.REGION + self.API_VERSION + "/item.json")
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
