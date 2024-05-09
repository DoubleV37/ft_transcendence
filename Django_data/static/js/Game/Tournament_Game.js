function launchGame () {
  gameSocket = new WebSocket(
    "wss://" + window.location.host + "/wss" + ROUTE.GAME_LOCAL
  );

  gameSocket.addEventListener("open", onOpenGame);
  gameSocket.addEventListener("close", onCloseGame);
  document.addEventListener("keyup", keyUp);
  document.addEventListener("keydown", keyDown);
  document.getElementById("Bracket").hidden = true;
  document.getElementById("Game").hidden = false;
  init_canvas();
}

function quitGame () {
  if (gameSocket.readyState === WebSocket.OPEN ||
      gameSocket.readyState === WebSocket.CONNECTING) {
    gameSocket.close();
  }
}

function onOpenGame () {
  console.log("The connection was setup successfully !");
  console.log(GameParams);

  gameSocket.send(JSON.stringify(GameParams));
  gameSocket.addEventListener("message", receiveGameMsg);
  gameStop = false;
  updateGame();
}

function onCloseGame () {
  console.log("The connection as ended!");
  gameStop = true;
  gameSocket.removeEventListener("message", receiveGameMsg);
  gameSocket.removeEventListener("open", onOpenGame);
  gameSocket.removeEventListener("close", onCloseGame);
  document.removeEventListener("keyup", keyUp);
  document.removeEventListener("keydown", keyDown);
  keyStates = {
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    s: false,
    space: false
  };
}

function receiveGameMsg (e) {
  const data = JSON.parse(e.data);

  console.log(data.message);
  if (gameSocket.readyState === WebSocket.CLOSING ||
      gameSocket.readyState === WebSocket.CLOSED) {
    return;
  }
  if (data.message === "game_state") {
    const score1div = document.getElementById("score1div");
    const score2div = document.getElementById("score2div");
    score1div.innerHTML = data.score1;
    score2div.innerHTML = data.score2;
    gameCanvas.ballRadius = data.ballsize * gameCanvas.height * 2;
    gameCanvas.paddle1Height = data.paddle1size * gameCanvas.height;
    gameCanvas.paddle2Height = data.paddle2size * gameCanvas.height;
    if (gameCanvas.powerup) {
      gameCanvas.powerupY = data.powerupY;
      gameCanvas.powerupsize = data.powerupsize;
    }
    draw(data);
  }
  if (data.message === "game_finish") {
    console.log(data.winner);
    data.winner === "Guest" ? updateMatch(1) : updateMatch(2);
  }
}

function updateMatch (team) {
  players = [];

  for (let i = 1; i < 5; i++) {
    if (tournament[`P${i}`].match === tournament.match) {
      players.push(tournament[`P${i}`]);
    }
  }
  if (players[0].team !== team) {
    players.reverse();
  }
  endMatch(players[0].username);
  if (tournament.match === 3) {
    tournament.winner = players[0].username;
    players[1].winner = false;
    players[0].winner = true;
  } else {
    players[1].winner = false;
    players[0].team = players[0].match === 1 ? 1 : 2;
    futurPlayer = firstPlayerInFinal();
    console.log(`futur player => ${futurPlayer}`);
    if (futurPlayer !== null) {
      players[0].vs = futurPlayer.username;
      futurPlayer.vs = players[0].username;
    } else {
      players[0].vs = "";
    }
    players[0].match = 3;
    tournament.match = tournament.match === 1 ? 2 : 3;
  }
}

function firstPlayerInFinal () {
  for (let i = 1; i < 5; i++) {
    if (tournament[`P${i}`].match === 3) {
      return tournament[`P${i}`];
    }
  }
  return null;
}

function updateGame () {
  if (gameSocket.readyState === WebSocket.CLOSED ||
      gameSocket.readyState === WebSocket.CLOSE) {
    return ;
  }
  if (gameStop !== true) {
    if (keyStates.ArrowUp) {
      gameSocket.send(JSON.stringify({ message: "up" }));
    } else if (keyStates.ArrowDown) {
      gameSocket.send(JSON.stringify({ message: "down" }));
    } else if (keyStates[" "]) {
      gameSocket.send(JSON.stringify({ message: "space" }));
    }
    if (keyStates.w) {
      gameSocket.send(JSON.stringify({ message: "w" }));
    } else if (keyStates.s) {
      gameSocket.send(JSON.stringify({ message: "s" }));
    }
    // Planifiez la prochaine mise à jour
    requestAnimationFrame(updateGame);
  }
}

function endMatch (message) {
  const endGameScreen = document.getElementById("endGameScreen");
  const endGameMessage = document.getElementById("endGameMessage");
  const confirmEndGame = document.getElementById("confirmEndGame");

  if (gameSocket != null) {
    gameSocket.close();
  }
  document.getElementById("MyCanvas").hidden = true;
  endGameMessage.textContent = `${message} won the match!`;
  endGameScreen.style.display = "flex";
  confirmEndGame.onclick = function () {
    bracket_SetEvents();
    endGameScreen.style.display = "none";
    document.getElementById("MyCanvas").hidden = false;
    document.getElementById("Bracket").hidden = false;
    document.getElementById("Game").hidden = true;
  };
  gameCanvas.inGame = false;
}
