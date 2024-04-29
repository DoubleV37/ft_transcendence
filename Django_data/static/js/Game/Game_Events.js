function game_SetEvents () {
  // document.addEventListener('resize', ResizeCanvas);
  gameStop = false;
  gameSocket = new WebSocket("wss://" + window.location.host + "/wss" + window.location.pathname);
  gameSocket.addEventListener('message', SetTheGame);
  gameSocket.addEventListener("open", OnOpenCallback);
  gameSocket.addEventListener("close", OnCloseCallback);
  init_canvas();
}

function game_DelEvents () {
  console.log("game_DelEvents");
  // document.removeEventListener('resize', ResizeCanvas);
  document.removeEventListener("keyup", keyUp);
  document.removeEventListener("keydown", keyDown);

  gameSocket.close();

  keyStates = {
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    s: false,
    space: false
  };
}

function SetTheGame (event) {
  //const data = JSON.parse(event.data);

  //Set the differents infos of the Game
  //Player name, profilePictures, skins ...
  //if (data.context === "GameInfos") { 
    //parseUserInfos(data);
    //setGameScreen();
    gameSocket.removeEventListener('message', SetTheGame);
    gameSocket.addEventListener("message", receive_data);
    document.addEventListener("keyup", keyUp);
    document.addEventListener("keydown", keyDown);
    update();
  //}
}

function OnOpenCallback () {
  console.log("The connection was setup successfully !");
  //LoadingState = true;
  gameSocket.addEventListener('message', SetTheGame);
  const name = document.getElementById("titleContent").getAttribute("data-content");

  if (name === "GAME_LOCAL") {
    console.log(GameParams);
    gameCanvas.powerup = GameParams.powerup;
    gameSocket.send(JSON.stringify(GameParams));
  } else if (name === "GAME_ROOM") {
    gameCanvas.powerup = false;
    GameParams.point_limit = 1;
    gameSocket.send(JSON.stringify(GameParams));
  }
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

// function ResizeCanvas() {
//  style = getComputedStyle(canvas);
//  width = parseInt(style.getPropertyValue('width'), 10);
//  height = parseInt(style.getPropertyValue('height'), 10);
//  canvas.width = width;
//  canvas.height = height;
//}
