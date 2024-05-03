function game_SetEvents () {
  gameStop = false;
  gameSocket = new WebSocket("wss://" + window.location.host + "/wss" + window.location.pathname);
  gameSocket.addEventListener("message", SetTheGame);
  gameSocket.addEventListener("open", OnOpenCallback);
  gameSocket.addEventListener("close", OnCloseCallback);
  init_canvas();
}

function game_DelEvents () {
  console.log("game_DelEvents");
  // document.removeEventListener('resize', ResizeCanvas);
  document.removeEventListener("keyup", keyUp);
  document.removeEventListener("keydown", keyDown);
  if (gameSocket !== null && gameSocket.readyState === WebSocket.OPEN) {
    if (gameCanvas.inGame == true) {
      gameSocket.send(JSON.stringify({ message: "stop" }));
      gameCanvas.inGame = false;
    }
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

function SetTheGame (event) {
  const data = JSON.parse(event.data);

  parseUserInfos(data);
  setGameScreen();

  gameSocket.removeEventListener("message", SetTheGame);
  gameSocket.addEventListener("message", receive_data);
  document.addEventListener("keyup", keyUp);
  document.addEventListener("keydown", keyDown);
  update();
}

function OnOpenCallback () {
  console.log("The connection was setup successfully !");
  gameSocket.addEventListener("message", SetTheGame);

  if (window.location.pathname === "/game/solo/") {
    console.log(GameParams);
    gameCanvas.powerup = GameParams.powerup;
  } else {
    gameCanvas.powerup = false;
    GameParams.point_limit = 1;
    GameParams.type = "remote";
    GameParams.opponent = "player";
  }
  gameSocket.send(JSON.stringify(GameParams));
}

function OnCloseCallback () {
  gameSocket.removeEventListener("message", receive_data);
  gameSocket.removeEventListener("open", OnOpenCallback);
  gameSocket.removeEventListener("close", OnCloseCallback);

  console.log("Socket was closed!");
  gameSocket = null;
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

function init_canvas () {
  gameCanvas.canvas = document.getElementById("MyCanvas");
  gameCanvas.ctx = gameCanvas.canvas.getContext("2d");
  gameCanvas.style = getComputedStyle(gameCanvas.canvas);
  gameCanvas.width = parseInt(gameCanvas.style.getPropertyValue("width"), 10);
  gameCanvas.height = parseInt(gameCanvas.style.getPropertyValue("height"), 10);
  gameCanvas.canvas.width = gameCanvas.width;
  gameCanvas.canvas.height = gameCanvas.height;
}
