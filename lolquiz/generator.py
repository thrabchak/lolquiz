from lolapi import LolApi, RiotApiService, SummonerSpell
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
    #self.createChampionAbilitiesCards()
    self.createSummonerSpellCards()
    self.flashcards.saveCards()
    return

  def createChampionAbilitiesCards(self):
    """Returns list of all champion ability cards"""
    championsList = self.lol.getChampions()
    for champion in championsList:
      card = ChampionAbilitiesCard(champion)
      championsList.append(card)
    return championsList

  def createSummonerSpellCards(self):
    summonerSpells = self.lol.getSummonerSpells()
    for spell in summonerSpells:
      question = "What is the cooldown of {0}?".format(spell.getName())
      answer = spell.getCooldownString()
      card = Card(question, answer, ["summonerSpell"])
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
    cardFactory.createAllCards()
  except Exception as e:
    print("Error generating cards.")
    print(e)
    exit(-1)

  print("Flash cards created successfully.")
  return   

if __name__ == '__main__':
  main()
