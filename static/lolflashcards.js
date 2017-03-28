
window.onload = function()
{
  getCard();
};

function getCard()
{
  httpGetAsync("card", function(response) {
    var card = JSON.parse(response);
    document.getElementById("card_text").textContent = card.question;
  })
};

function httpGetAsync(theUrl, callback)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
    }
  xmlHttp.open("GET", theUrl, true); // true for asynchronous 
  xmlHttp.send(null);
};
