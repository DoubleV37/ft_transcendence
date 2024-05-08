function lauchGame () {
  gameSocket = new WebSocket(
    "wss://" + window.location.host + "/wss" + ROUTE.GAME_LOCAL
  );
  gameSocket.addEventListener("message", receiveGameMsg);
  gameSocket.addEventListener("open", onOpenGame);
  gameSocket.addEventListener("close", onCloseGame);
  document.addEventListener("keyup", keyUp);
  document.addEventListener("keydown", keyDown);
  document.getElementById("Bracket").hidden = true;
  document.getElementById("Game").hidden = false;
}

function onOpenGame () {
  console.log("The connection was setup successfully !");
  gameSocket.addEventListener("message", SetTheGame);

  gameSocket.send(JSON.stringify(GameParams));
  gameStop = false;
  updateGame();
}

function onCloseGame () {
  gameStop = true;
  gameSocket.removeEventListener("message", receiveGameMsg);
  gameSocket.removeEventListener("open", onOpenGame);
  gameSocket.removeEventListener("close", onCloseGame);
  document.removeEventListener("keyup", keyUp);
  document.removeEventListener("keydown", keyDown);
}

function receiveGameMsg (e) {
  const data = JSON.parse(e.data);

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
    if (data.winner === "guest") {
      updateMatch(1);
      endMatch(GameInfos.PlayerL.username);
    } else {
      updateMatch(2);
      endMatch(GameInfos.PlayerL.username);
    }
  }
}

function updateMatch (team) {
  players = [];

  for (let i = 1; i < 5; i++) {
    if (tournament[`P${i}`].match === tournament.match) {
      players.push(tournament[`P${i}`]);
    }
  }
  if (player[0].team !== team) {
    players.reverse();
  }
  if (tournament.match === "3") {
    tournament.winner = player[0].team === 1 ? player[0].username : player[1].username;
    players[1].winner = false;
  } else {
    players[1].winner = false;
    player[0].team = player[0].match === 1 ? 1 : 2;
    players[0].match = 3;
    futurPlayer = firstPlayerInFinal();
    if (futurPlayer !== null) {
      player[0].vs = futurPlayer.username;
      futurPlayer.vs = player[0].username;
    }
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
  if (gameStop !== true) {
    requestAnimationFrame(update);
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
    document.getElementById("Bracket").hidden = true;
    document.getElementById("Game").hidden = false;
  };
  gameCanvas.inGame = false;
}
