import argparse

from lolapi import LolApi, RiotApiService, SummonerSpell, Champion
from flashcards import Card, CardStorage
from filesystem import FileSystemService


class CardFactory(object):
  """Class used to create flash cards."""

  CHAMPION_ABILITIES_CATEGORY="Champion Abilities"
  SUMMONER_SPELLS_CATEGORY="Summoner Spells"
  ITEMS_CATEGORY="Items"

  def __init__(self, fileSystemService=None, riotApiService=None, flashcards=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    if(riotApiService != None):
      self.riotApiService = riotApiService
    else:
      self.riotApiService = RiotApiService()
    
    if(flashcards != None):
      self.flashcards = flashcards
    else:
      self.flashcards = CardStorage(self.fileSystemService)

    self.lol = LolApi(self.fileSystemService, self.riotApiService)

  def updateData(self):
    """Ensures that we have the latest LoL data downloaded."""
    # see if we already have static data downloaded. if not, download
    if(not self.lol.isUpToDate()):
      print("Not up to date")
      self.lol.downloadDataFiles()
    return

  def createAllCards(self):
    """Creates all flash cards and saves them to disk as a JSON file."""
    self.createChampionAbilitiesCards()
    # self.createSummonerSpellCards()
    # self.createItemCards()
    return self.flashcards

  def createChampionAbilitiesCards(self):
    """Returns list of all champion ability cards"""
    championsList = self.lol.getChampions()
    for champ in championsList:
      print(champ.getName())
      detailedChamp = self.lol.getChampion(champ.jsonData["id"])
      abilities = detailedChamp.getAbilitiesAsStrings()
      question = "What are {0}'s abilities?".format(detailedChamp.getName())
      answer = r"Passive: {0}\n\nQ: {1}\n\nW: {2}\n\nE: {3}\n\nR: {4}\n".format(abilities[0], abilities[1], abilities[2], abilities[3], abilities[4])
      card = Card(question, answer, [self.CHAMPION_ABILITIES_CATEGORY])
      self.flashcards.addCard(card)
    return

  def createSummonerSpellCards(self):
    summonerSpells = self.lol.getSummonerSpells()
    for spell in summonerSpells:
      question = "What is the cooldown of {0}?".format(spell.getName())
      answer = spell.getCooldownString()
      card = Card(question, answer, [self.SUMMONER_SPELLS_CATEGORY])
      self.flashcards.addCard(card)
    return

  def createItemCards(self):
    items = self.lol.getItems()
    for item in items:
      question = "What is {0}?".format(item.getName())
      answer = item.description()
      card = Card(question, answer, [self.ITEMS_CATEGORY])
      self.flashcards.addCard(card)
    return

class HtmlCardFactory(CardFactory):
  """This class behaves very much like CardFactory, except that it stores the question and answer as html
  instead of plain text"""

  def createChampionAbilitiesCards(self):
    """Returns list of all champion ability cards"""
    championsList = self.lol.getChampions()
    for champ in championsList:
      abilities = champ.getAbilitiesAsHtml()
      question = "What are {0}'s abilities?".format(champ.getName())
      answer = "Passive: {0}<br><br>Q: {1}<br><br>W: {2}<br><br>E: {3}<br><br>R: {4}<br><br>".format(abilities[0], abilities[1], abilities[2], abilities[3], abilities[4])
      card = Card(question, answer, [self.CHAMPION_ABILITIES_CATEGORY])
      self.flashcards.addCard(card)
    return

  def createSummonerSpellCards(self):
    summonerSpells = self.lol.getSummonerSpells()
    for spell in summonerSpells:
      question = "What is the cooldown of {0}?".format(spell.getName())
      answer = spell.getCooldownString()
      card = Card(question, answer, [self.SUMMONER_SPELLS_CATEGORY])
      self.flashcards.addCard(card)
    return

  def createItemCards(self):
    items = self.lol.getItems()
    for item in items:
      question = "What is {0}?".format(item.getName())
      answer = item.html()
      card = Card(question, answer, [self.ITEMS_CATEGORY])
      self.flashcards.addCard(card)
    return

def main():
  parser = argparse.ArgumentParser(description="Generates Leauge of Legends flashcards and stores them in a json file.")
  parser.add_argument("--html", help="Generates html cards instead of plain text cards.",
                    action="store_true")
  args = parser.parse_args()

  if(args.html):
    cardFactory = HtmlCardFactory()
    print("Generating HTML flashcards.")
  else:
    cardFactory = CardFactory()

  try:
    cardFactory.updateData()
  except Exception as e:
    print("Error updating lol static data to most recent version.")
    print(e)
    exit(-1);

  try:
    cards = cardFactory.createAllCards()
    print('saving')
    cards.saveCards()
  except Exception as e:
    print("Error generating cards.")
    print(e)
    exit(-1)

  print("Flash cards created successfully.")
  return   

if __name__ == '__main__':
  main()
