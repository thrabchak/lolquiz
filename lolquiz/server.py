import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

import threading

from timeit import default_timer as timer
from tornado.options import define, options

from generator import HtmlCardFactory
from flashcards import CardStorage

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", HomeHandler),
      (r"/about", AboutHandler),
      (r"/card", CardHandler),
    ]
    settings = dict(
        blog_title=u"LoL Flash Cards",
        template_path=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "..", "static"),
        debug=True,
    )

    super(Application, self).__init__(handlers, **settings)

    # Load existing flashcards
    self.cards = self.loadFlashCards()

    # Asynchronously create new flashcards
    self.cardsLock = threading.Lock()
    t = threading.Thread(name="create_new_cards", target=self.createFlashcards)
    t.start()

  def loadFlashCards(self):
    cardStorage = CardStorage()
    cardStorage.load()
    return cardStorage

  def createFlashcards(self):
    start = timer()

    cardFactory = HtmlCardFactory()

    try:
      cardFactory.updateData()
    except Exception as e:
      print("Error updating lol static data to most recent version.")
      print(e)
      exit(-1);

    try:
      cards = cardFactory.createAllCards()
      print("Flash cards created successfully.")
      end = timer()
      print("Total: {0}".format(cards.count()))
      print("Time: {0}".format(end-start))
      print("Categories: {0}".format(cards.validCategories()))
    except Exception as e:
      print("Error generating cards.")
      print(e)
      exit(-1)

    try:
      self.cardsLock.acquire()
      self.cards = cards
    finally:
      self.cardsLock.release()
    return None

class BaseHandler(tornado.web.RequestHandler):
  @property
  def cards(self):
    return self.application.cards

  @property
  def cardsLock(self):
    return self.application.cardsLock

class HomeHandler(BaseHandler):
  def get(self):
    self.render("base.html", title="LoL Flash Cards")

class AboutHandler(BaseHandler):
  def get(self):
    self.write("About page")

class CardHandler(BaseHandler):
  def get(self):
    categories = []
    if(self.get_arguments("champs")):
      categories.append(HtmlCardFactory.CHAMPION_ABILITIES_CATEGORY)
    if(self.get_arguments("items")):
      categories.append(HtmlCardFactory.ITEMS_CATEGORY)
    if(self.get_arguments("summs")):
      categories.append(HtmlCardFactory.SUMMONER_SPELLS_CATEGORY)

    try:
      self.cardsLock.acquire()
      card = self.cards.drawRandomCard(categories)
    finally:
      self.cardsLock.release()

    self.write(card.toJson())

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  port = int(os.environ.get("PORT", 5000))
  http_server.listen(port)
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
    exit(1)

if __name__ == "__main__":
    main()
