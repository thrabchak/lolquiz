from lolapi import LolApi
from flashcards import Card, CardStorage

class CardFactory(object):
  """Class used to create flash cards."""

  def updateData(self):
    """Ensures that we have the latest LoL data downloaded."""
    # see if we already have static data downloaded. if not, download

    # if we have static data, check it's version
    # get current data dragon version from api
    # compare versions, if different, download
    pass

  def createAllCards(self):
    """Creates all flash cards and saves them to disk as a JSON file."""
    championsAbilitiesCards = self.createChampionAbilitiesCards()
    saveAllCardsAsJson(championsAbilitiesCards)

  def saveAllCardsAsJson(self, cards):
    """Saves all the generated cards as JSON""" 
    cardsList = ['{']
    for card in cards:
      cardsList.append(card.toJson())
      cardsList.append(',')
    cardsList.pop()
    cardsList.append('}')

    big_string = ''.join(cardsList)
    #save big_string
    #alternatively write every entry in cardsList to a new line in the file
    pass

  def createChampionAbilitiesCards(self):
    """Returns list of all champion ability cards"""
    championsList = lolapi.getChampions()
    for champion in championsList:
      card = ChampionAbilitiesCard(champion)
      championsList.append(card)
    return championsList

class ChampionAbilitiesCard(Card):
  """Class for asking questions about champions."""
  def __init__(self, champion):

    pass

def main():
  cardFactory = CardFactory()

  try:
    qFactory.updateData()
  except Exception as e:
    print("Error updating lol static data to most recent version.")
    exit(-1);

  try:
    qFactory.createAllCards()
  except Exception as e:
    print("Error generating cards.")
    exit(-1)

  print("Flash cards created successfully.")
  return   

if __name__ == '__main__':
  main()