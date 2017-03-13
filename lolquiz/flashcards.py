import random
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

  def load(self):
    cardsJson = self.fileSystemService.readJsonFile(self.CARD_FILE)
    for c in cardsJson["flashcards"]:
      card = Card(c["question"], c["answer"], c["categories"])
      self.addCard(card)
    if(len(self.cards) == 0):
      raise Exception("No cards loaded.")
    return

  def drawRandomCard(self):
    return self.cards[random.randint(0, len(self.cards) - 1)]

class Quiz(object):
  """docstring for Quiz"""
  def __init__(self, fileSystemService=None, ioService=None):
    if(fileSystemService != None):
      self.fileSystemService = fileSystemService
    else:
      self.fileSystemService = FileSystemService()

    if(ioService != None):
      self.io = ioService
    else:
      self.io = IoService()

    self.flashcards = CardStorage(self.fileSystemService)
    self.counter = 0

  def loop(self):
    self.start()

    continueQuiz = True
    while (continueQuiz):
      self.counter += 1
      card = self.flashcards.drawRandomCard()
      self.io.printQuestion(card.question)
      continueQuiz = self.io.waitForInput()
      self.io.printAnswer(card.answer)
      
    self.end()
    return

  def start(self):
    try:
      self.flashcards.load()
    except Exception as e:
      print("Error loading flashcards.")
      print(e)
      raise e

    self.io.printInfo("Found {0} flashcards to quiz from.".format(len(self.flashcards.cards)))
    self.io.printInfo("Starting quiz.")
    return

  def end(self):
    # end quiz loop
    self.io.printInfo("Quizzed on {0} flashcards.".format(self.counter))
    return

class IoService():

  def printInfo(self, string):
    print(string)
    return

  def printQuestion(self, string):
    print(string)
    return

  def printAnswer(self, string):
    print(string)
    print("\n=======\n")
    return

  def waitForInput(self):
    text = input()
    if(text != ""):
      return False
    return True

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
