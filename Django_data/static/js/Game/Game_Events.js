function game_SetEvents () {
	if (window.location.pathname === "/game/solo/")
		gameSocket = new WebSocket("wss://" + window.location.host + "/wss" + window.location.pathname);
	else
		gameSocket = new WebSocket("wss://" + window.location.host + "/ws/multi" + window.location.pathname);
	gameSocket.addEventListener("message", SetTheGame);
	gameSocket.addEventListener("open", OnOpenCallback);
	gameSocket.addEventListener("close", OnCloseCallback);
	init_canvas();

  document.body.addEventListener("mousedown", mousedown);
  document.body.addEventListener("mouseup", mouseup);
}

function game_DelEvents () {
  document.removeEventListener("keyup", keyUp);
  document.removeEventListener("keydown", keyDown);
  document.body.removeEventListener("mousedown", mousedown);
  document.body.removeEventListener("mouseup", mouseup);
  if (loading === true) {
	gameSocket.removeEventListener("message", SetTheGame);
  } else {
	gameSocket.removeEventListener("message", receive_data);
  }
  if (gameCanvas.inGame == true) {
	gameCanvas.inGame = false;
	gameSocket.send(JSON.stringify({ message: "stop" }));
	gameSocket.send(JSON.stringify({ message: "stopGame" }));
	wait_and_close();
  } else {
	gameSocket.close();
  }

  keyStates = {
	ArrowUp: false,
	ArrowDown: false,
	w: false,
	s: false,
	space: false
  };
}

async function wait_and_close () {
  sleep(1000);
  gameSocket.close(1000);
}

function SetTheGame (event) {
  const data = JSON.parse(event.data);

  loading = true;
  gameCanvas.inGame = true;
  if (data.message === "Game stopped") {
	if (deleteEvent === true) {
	  return;
	}
	gameSocket.removeEventListener("message", SetTheGame);
	EndGame("Game already finished!");
  } else {
	if (deleteEvent === true) {
	  return;
	}
	parseUserInfos(data);
	setGameScreen();
	gameSocket.removeEventListener("message", SetTheGame);
	gameSocket.addEventListener("message", receive_data);
	document.addEventListener("keyup", keyUp);
	document.addEventListener("keydown", keyDown);
	update();
  }
  loading = false;
}

function OnOpenCallback () {
  gameStop = false;
  gameSocket.addEventListener("message", SetTheGame);
  gameCanvas.powerup = GameParams.powerup;
  gameSocket.send(JSON.stringify(GameParams));
}

function OnCloseCallback () {
  gameSocket.removeEventListener("message", receive_data);
  gameSocket.removeEventListener("open", OnOpenCallback);
  gameSocket.removeEventListener("close", OnCloseCallback);

  gameStop = true;
}

function keyUp (e) {
  keyStates[e.key] = false;
}

function keyDown (e) {
  if (e.key !== "F5" && !(e.key === "F5" && e.ctrlKey) && e.key !== "F12") {
	  e.preventDefault();
  }
  keyStates[e.key] = true;
}

function mouseup (e) {
  whichMove(e, false);
}

function mousedown (e) {
  whichMove(e, true);
}

function whichMove (e, value) {
  const rect = document.body.getBoundingClientRect();
  const pos = getMousePosition(e, rect);
  const vLine = rect.x + rect.width / 2;
  const hLine = rect.y + rect.height / 2;
  if (pos.x < vLine - 1 && pos.y < hLine - 1) {
    keyStates['w'] = value; 
  } else if (pos.x < vLine - 1 && pos.y > hLine + 1) {
    keyStates['s'] = value;
  } else if (pos.x > vLine + 1 && pos.y < hLine - 1) {
    keyStates['ArrowUp'] = value;
  } else if (pos.x > vLine + 1 && pos.y > hLine + 1) {
    keyStates['ArrowDown'] = value;
  }
}

function getMousePosition (e, rect) {
  const pos = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
  return pos;
}

function init_canvas () {
  gameCanvas.canvas = document.getElementById("MyCanvas");
  gameCanvas.ctx = gameCanvas.canvas.getContext("2d");
  gameCanvas.style = getComputedStyle(gameCanvas.canvas);
  gameCanvas.width = parseInt(gameCanvas.style.getPropertyValue("width"), 10);
  gameCanvas.height = parseInt(gameCanvas.style.getPropertyValue("height"), 10);
  gameCanvas.canvas.width = gameCanvas.width;
  gameCanvas.canvas.height = gameCanvas.height;
  gameCanvas.paddle1Height = 0,
  gameCanvas.paddle2Height = 0,
  gameCanvas.powerup = false,
  gameCanvas.powerupY = 0,
  gameCanvas.powerupX = 0,
  gameCanvas.powerupsize = 0,
  gameCanvas.ballRadius = 0,
  gameCanvas.opponent = "",
  gameCanvas.num = 0,
  gameCanvas.inGame = true;
}
