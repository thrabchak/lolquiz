from flashcards import Card, CardStorage
import test_utils

class TestCardStorage:

  def setup(self):
    self.fs = test_utils.MockFileSystemService()
    self.storage = CardStorage(self.fs)

  def test_addCard(self):
    card = Card("Test", "test", [])
    self.storage.addCard(card)
    assert len(self.storage.cards) == 1
    assert self.storage.cards[0].question == "Test"
    assert self.storage.cards[0].answer == "test"

  def test_addCards(self):
    card1 = Card("Test", "test", [])
    card2 = Card("Test2", "test2", [])
    self.storage.addCard(card1)
    self.storage.addCard(card2)
    assert len(self.storage.cards) == 2
    assert self.storage.cards[0].question == "Test"
    assert self.storage.cards[0].answer == "test"
    assert self.storage.cards[1].question == "Test2"
    assert self.storage.cards[1].answer == "test2"

  def test_addCardsWithCategories(self):
    card1 = Card("Test", "test", ["cat1"])
    card2 = Card("Test2", "test2", ["cat2", "cat3"])    
    self.storage.addCard(card1)
    self.storage.addCard(card2)
    assert len(self.storage.cards) == 2
    assert "cat1" in self.storage.cards[0].categories
    assert "cat2" in self.storage.cards[1].categories
    assert "cat3" in self.storage.cards[1].categories
    assert "cat1" not in self.storage.cards[1].categories

  def test_saveCard(self):
    card = Card("Test", "test", ["cat1"])
    self.storage.addCard(card)
    self.storage.saveCards()
    assert self.fs.valueMap["flashcards.json"] == '{"flashcards": [{"answer": "test", "categories": ["cat1"], "question": "Test"}]}'
  
  def test_saveCards(self):
    card1 = Card("Test", "test", ["cat1"])
    card2 = Card("Test2", "test2", ["cat2", "cat3"])    
    self.storage.addCard(card1)
    self.storage.addCard(card2)
    self.storage.saveCards()
    assert self.fs.valueMap["flashcards.json"] == '{"flashcards": [{"answer": "test", "categories": ["cat1"], "question": "Test"}, {"answer": "test2", "categories": ["cat2", "cat3"], "question": "Test2"}]}'
