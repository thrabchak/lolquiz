from lolapi import LolApi, RiotApiService, SummonerSpell, Champion
from flashcards import Card, CardStorage
from filesystem import FileSystemService

class CardFactory(object):
  """Class used to create flash cards."""
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
      self.lol.downloadDataFiles()
    return

  def createAllCards(self):
    """Creates all flash cards and saves them to disk as a JSON file."""
    self.createChampionAbilitiesCards()
    self.createSummonerSpellCards()
    self.createItemCards()
    return self.flashcards

  def createChampionAbilitiesCards(self):
    """Returns list of all champion ability cards"""
    championsList = self.lol.getChampions()
    for champ in championsList:
      abilities = champ.getAbilitiesAsStrings()
      question = "What are {0}'s abilities?".format(champ.getName())
      answer = r"Passive: {0}\n\nQ: {1}\n\nW: {2}\n\nE: {3}\n\nR: {4}\n".format(abilities[0], abilities[1], abilities[2], abilities[3], abilities[4])
      card = Card(question, answer, ["Champion Abilities"])
      self.flashcards.addCard(card)
    return

  def createSummonerSpellCards(self):
    summonerSpells = self.lol.getSummonerSpells()
    for spell in summonerSpells:
      question = "What is the cooldown of {0}?".format(spell.getName())
      answer = spell.getCooldownString()
      card = Card(question, answer, ["Summoner Spells"])
      self.flashcards.addCard(card)
    return

  def createItemCards(self):
    items = self.lol.getItems()
    for item in items:
      question = "What is {0}?".format(item.getName())
      answer = item.description()
      card = Card(question, answer, ["Items"])
      self.flashcards.addCard(card)
    return

def main():
  cardFactory = CardFactory()

  try:
    cardFactory.updateData()
  except Exception as e:
    print("Error updating lol static data to most recent version.")
    print(e)
    exit(-1);

  try:
    cards = cardFactory.createAllCards()
    cards.saveCards()
  except Exception as e:
    print("Error generating cards.")
    print(e)
    exit(-1)

  print("Flash cards created successfully.")
  return   

if __name__ == '__main__':
  main()
