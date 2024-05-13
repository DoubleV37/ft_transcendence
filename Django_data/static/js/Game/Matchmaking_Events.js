function matchmaking_SetEvents () {
  matchSocket = new WebSocket("wss://" + window.location.host + "/ws/multi/matchmaking/");

  matchSocket.onopen = function () {
    matchSocket.send(JSON.stringify(GameParams));
  };

  matchSocket.onmessage = function (event) {
    data = JSON.parse(event.data);
	if (data.message == "settings") {
	  GameParams = data;
	}
    if (data.message == "match_found") {
      matchSocket.close();
      loadPage(`${ROUTE.GAME_ROOM}${data.room_name}/`);
    }
  };

  matchSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };
}

function matchmaking_DelEvents () {
  matchSocket.close();
}
