async function modes_randomMatchmaking() {
	try {
		await loadPage(`${ROUTE.GAME_MATCH}`);
	} catch (error) {
		console.log(`Error - playerVSplayer: ${error}`);
	}
}

async function modes_playerVSia() {
	try {
		GameParams.opponent = "ai";
		GameParams.type = "local";
		GameParams.point_limit = 3;
		GameParams.difficulty = 5;
		GameParams.powerup = false;
		await loadPage(`${ROUTE.GAME_LOCAL}`);
	} catch (error) {
		console.log(`Error - playerVSia: ${error}`);
	}
}

function modes_ChooseGame() {
  console.log("ChooseGame: do nothing for now");
}

async function modes_CreateGame() {
  await loadPage(`${ROUTE.GAME_PARAMETERS}`);
}

function modes_ChooseTournament() {
  console.log("ChooseTournament: do nothing for now");
}

function modes_CreateTournament() {
  console.log("CreateTournament: do nothing for now");
}

function MultiTestCallback (event) {
  event.target.removeEventListener("click", MultiTestCallback);
  event.target.setAttribute("class", "MediumButtonLayout right ButtonDark");

  const element = document.getElementById("MultiSend");
  element.setAttribute("class", "MediumButtonLayout right ButtonNeon");
  const websocket = new WebSocket("wss://" + window.location.host + "/ws/multi/");

  websocket.onopen = () => {
    console.log("MultiTest Websocket openned!");
    websocket.send("Client: Connected.");
  }
  websocket.onclose = () => {
    console.log("MultiTest Websocket closed!");
    websocket.send("Client: Closed.");
  }
  websocket.onerror = () => {
    console.log("MultiTest Websocket error!");
    websocket.send("Client: Error.");
  }
  websocket.onmessage = (event) => {
	console.log(event.data);
    // const data = JSON.parse(event.data);
  }
  element.addEventListener("click", () => {
    console.log("Client: clicked!");
	websocket.send("coucou");
  });
}
