function matchmaking_SetEvents () {
  // Fonction pour se connecter au WebSocket
  matchSocket = new WebSocket("wss://" + window.location.host + "/wss/game/matchmaking");

  matchSocket.onopen = function () {
    console.log("WebSocket matchmaking connection established.");
    matchSocket.send("search");
  };

  matchSocket.onmessage = function (event) {
    //console.log("Message received from server:", event.data);
    data = JSON.parse(event.data);
    if (data.type == "match_found") {
      console.log("Match found:", data);
      matchSocket.close();
      loadPage(`${ROUTE.GAME_ROOM}${data.room_name}/`);
    }
  };

  matchSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };

  matchSocket.onclose = function (event) {
    console.log("WebSocket matchmaking connection closed:", event);
  };
}

function matchmaking_DelEvents () {
  matchSocket.close();
}