import json
from filesystem import FileSystemService

class Card(object):

  def __init__(self, question, answer, categories):
    self.question = question
    self.answer = answer
    self.categories = categories

  def toJson(self):
    categoriesList = ['[']
    for c in self.categories:
      categoriesList.append('"' + c + '"')
      categoriesList.append(",")
    if( len(categoriesList) > 1):
      categoriesList.pop()
    categoriesList.append(']')
    categoriesString = ''.join(categoriesList)
    jsonString = '{{"question":"{0}","answer":"{1}","categories":{2}}}'.format(self.question, self.answer, categoriesString)
    return jsonString

class CardStorage(object):
  CARD_FILE="flashcards.json"

  def __init__(self, fileSystemService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    self.cards = []

  def addCard(self, card):
    self.cards.append(card)
    return

  def saveCards(self):
    cardJson = json.loads('{"flashcards":' + self.createCardsJsonList() + '}')
    self.fileSystemService.saveJsonFile(cardJson, self.CARD_FILE)
    return

  def createCardsJsonList(self):
    cardsList = ['[']
    for c in self.cards:
      cardsList.append(c.toJson())
      cardsList.append(",")
    if( len(cardsList) > 1):
      cardsList.pop()
    cardsList.append(']')
    return "".join(cardsList)

class Quiz(object):
  """docstring for Quiz"""
  def __init__(self, fileSystemService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

  def loop(self):
    self.start()

    continueQuiz = true
    while (continueQuiz):
      card = self.getCard()
      
    self.end()

  def start(self):
    # start quiz loop
    pass

  def end(self):
    # end quiz loop
    pass

  def getCard(self):
    # retun a quiz card
    return Card("","",[])


def main():
  quiz = Quiz()
  try:
    quiz.loop()
  except Exception as e:
    print("Error encountered while running the quiz.")
    raise e
  return

if __name__ == '__main__':
  main()
