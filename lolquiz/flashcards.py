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
    self.categories = {}

  def addCard(self, card):
    self.cards.append(card)

    for category in card.categories:
      if(category in self.categories.keys()):
        self.categories[category].append(card)
      else:
        self.categories[category] = [card]

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

  def drawRandomCard(self, categories=None):
    if(categories == None or len(categories) < 1):
      return self.cards[random.randint(0, len(self.cards) - 1)]
    else:
      randomCategory = random.randint(0, len(categories) - 1)
      categoryCardList = self.categories[categories[randomCategory]]
      return categoryCardList[random.randint(0, len(categoryCardList) - 1)]

  def count(self):
    return len(self.cards)

  def validCategories(self):
    return self.categories.keys()

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
    self.categories = []

  def loop(self):
    self.start()

    continueQuiz = True
    while (continueQuiz):
      self.counter += 1
      card = self.flashcards.drawRandomCard(self.categories)
      self.io.printQuestion(card.question)
      continueQuiz = self.io.waitForContinueInput()
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
    categoriesList = self.flashcards.categories.keys()
    if(len(categoriesList) > 0):
      self.io.printInfo("Found {0} categories. Please choose one of the following:\n".format(len(categoriesList)))
      self.io.printInfo("[]: All")
      counter = 0
      categoryKeyList = []
      for key in categoriesList:
        self.io.printInfo("[{0}]: {1}".format(counter, key))
        counter += 1
        categoryKeyList.append(key)
      chosenInput = self.io.waitForInput()
      if(chosenInput == ""):
        self.io.printInfo("\nStarting quiz with all categories.\n")
        return

      if(int(chosenInput) in range(len(categoriesList))):
        selectedCategory = categoryKeyList[int(chosenInput)]
        self.categories.append(selectedCategory)
        self.io.printInfo("\nStarting quiz in selected category - [{0}]: {1}\n".format(int(chosenInput), selectedCategory))

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

  def waitForContinueInput(self):
    text = input()
    if(text != ""):
      return False
    return True

  def waitForInput(self):
    return input()

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
