from question import QuestionFactory, Question

def main():
  QuestionFactory qFactory = QuestionFactory()

  try:
    qFactory.updateData()
  except Exception as e:
    print("Error updating lol static data to most recent version.")
    exit(-1);

  while(True):
    question = qFactory.createRandomQuestion()
    print("Question:\n" + question.getQuestion() + "\n\n")
    print("Answer:\n" + answer.getAnswer() + "\n\n")

if __name__ == '__main__':
  main()