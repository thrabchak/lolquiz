import json

from abc import ABCMeta

DEFAULT_SETTINGS_JSON = """
{
  "champion": {
    "general_abilities": true,
    "ability_cooldowns": false,
  },
  "items": {
    "general_items": true
  },
  "summoner_spells": {
    "cooldowns": true
  },
  "masteries": {
    "descriptions" : true
  }
}
"""

class QuestionFactory(object):
  config = None

  """Class used to create questions."""
  def __init__(self):
    self.loadConfig()

  def loadConfig():
    """Loads the default settings json as shown above. In the future, allow these options to be specified in a file"""
    config = json.loads(DEFAULT_SETTINGS_JSON)

  def updateData(self):
    """Ensures that we have the latest data downloaded."""
    # see if we already have static data downloaded. if not, download

    # if we have static data, check it's version
    # get current data dragon version from api
    # compare versions, if different, download
    pass

  def createRandomQuestion(self):
    """Returns instantiated Question class"""
    pass

class Question(metaclass=ABCMeta):
  """Abstract base class for all question types."""

  @abstractmethod
  def getQuestion(self):
    return "Question is defined by the derived Question type."

  @abstractmethod
  def getAnswer(self):
    return "Answer is defined by the derived Question type."

class ChampionQuestion(Question):
  """Class for asking questions about champions."""
  def __init__(self, chanmpion):
    pass

  def getQuestion(self):
    pass
    
  def getAnswer(self):
    pass

