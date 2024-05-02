function matchmaking_SetEvents () {
  // Fonction pour se connecter au WebSocket
  gameSocket = new WebSocket("wss://" + window.location.host + "/wss/game/matchmaking");

  gameSocket.onopen = function () {
    console.log("WebSocket matchmaking connection established.");
    gameSocket.send("search");
  };

  gameSocket.onmessage = function (event) {
    //console.log("Message received from server:", event.data);
    data = JSON.parse(event.data);
    if (data.type == "match_found") {
      console.log("Match found:", data);
      gameSocket.close();
      loadPage(`${ROUTE.GAME_ROOM}${data.room_name}/`);
    }
  };

  gameSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };

  gameSocket.onclose = function (event) {
    console.log("WebSocket matchmaking connection closed:", event);
  };
}

function matchmaking_DelEvents () {
  gameSocket.close();
}
