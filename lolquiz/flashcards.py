def createCard(question, answer, categories):
  try:
    card = Card(question, answer, categories)
  except Exception as e:
    print("Error creating card.")
    raise e

  try:
    card.save()
  except Exception as e:
    print("Error saving card.")
    raise e

  return

class Card(object):
  """Base class for all Card types."""
  question = ""
  answer = ""
  categories = []

  def __init__(self, question, answer, categories):
    self.question = question
    self.answer = answer
    self.categories = categories

  def toJson(self):
    categoriesList = ['[']
    for c in categories:
      categoriesList.append('"' + c + '"')
      categoriesList.append(",")
    categoriesList.pop()
    categoriesList.append(']')
    categoriesString = ''.join(categoriesList)
    return '{"question": "{0}", "answer":"{1}","categories":{2}}'.format(question, answer, categoriesString)

  def save(self):
    # Save flash card to default location

class Quiz(object):
  counter = 0

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
