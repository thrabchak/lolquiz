import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from timeit import default_timer as timer
from tornado.options import define, options

from generator import CardFactory
from flashcards import CardStorage

define("port", default=5000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", HomeHandler),
      (r"/card", CardHandler),
    ]
    settings = dict(
        blog_title=u"LoL Flash Cards",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )

    super(Application, self).__init__(handlers, **settings)
    self.cards = self.createFlashcards()

  def createFlashcards(self):
    start = timer()

    cardFactory = CardFactory()

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
      return cards
    except Exception as e:
      print("Error generating cards.")
      print(e)
      exit(-1)

    return None

class BaseHandler(tornado.web.RequestHandler):
  @property
  def cards(self):
    return self.application.cards

class HomeHandler(BaseHandler):
  def get(self):
    self.write("Home page")

class CardHandler(BaseHandler):
  def get(self):
    card = self.cards.drawRandomCard()
    self.write(card.question)

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
    exit(1)

if __name__ == "__main__":
    main()
