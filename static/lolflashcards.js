var LolQuiz = {};

LolQuiz.ClientApp = function() {
  this.textElem = document.getElementById("card_text");
  this.cards = [];
  this.showingFront = true;
  this.current = -1;
  this.registerButtonCallbacks();
};

LolQuiz.ClientApp.prototype = {

  registerButtonCallbacks() {
    var that = this;
    document.getElementById("flip_button").addEventListener("click", function() {that.flip();});
    document.getElementById("next_button").addEventListener("click", function() {that.next();});
    document.getElementById("prev_button").addEventListener("click", function() {that.prev();});
    window.addEventListener("keydown", function(e) {that.keyEvent(e)});
  },

  drawRandomCard: function() {
    var that = this;
    httpGetAsync("card", function(response) {
      var card = JSON.parse(response);
      that.cards.push(card);
      that.showCard(that.cards.length-1);
    });
  },

  showCard: function(i) {
    this.current = i;
    var card = this.cards[i];
    this.textElem.textContent = card.question;
    this.showingFront = true;
  },

  flip: function() {
    if(this.showingFront) {
      this.textElem.textContent = this.cards[this.current].answer;
      this.showingFront = false;
    } else {
      this.textElem.textContent = this.cards[this.current].question;
      this.showingFront = true;
    }
  },

  prev: function() {
    if(this.current-1 >= 0) {
      this.showCard(this.current-1);
    }
  },

  next: function() {
    if(this.current < this.cards.length-1) {
      this.showCard(this.current+1);
    } else {
      this.drawRandomCard();
    }
  },

  keyEvent: function(e) {
    var keyValue = e.keyCode;
    if([32, 37, 38, 39, 40].indexOf(keyValue) > -1) {
        e.preventDefault();
    }
    switch(keyValue) {
      case 13: // 13 is Enter
      case 32: // 32 is spacebar
        if(this.showingFront)
          this.flip();
        else
          this.next();
        break;
      case 37: // 37 is left
        this.prev();
        break;
      case 38: // 38 is up
        break;
      case 39: // 39 is right
        this.next();
        break;
      case 40: // 40 is down
        this.flip();
        break;
    }
  }

};

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
    }
  xmlHttp.open("GET", theUrl, true); // true for asynchronous 
  xmlHttp.send(null);
};

window.onload = function() {
  var clientApp = new LolQuiz.ClientApp();
  clientApp.drawRandomCard();
};
