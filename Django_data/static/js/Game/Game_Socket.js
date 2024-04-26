function init_websocket () {
  // Create WebSocket connection.
  gameSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
  };
  gameSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
  };
}

// ai_town
function iaBrain (data) {
  const rand = Math.floor(Math.random() * 41) - 20;
  let bx = data.ballX * 1200;
  let by = data.ballY * 900;
  const sx = data.ballspeedX;
  let sy = data.ballspeedY;
  iaMemory.pos = data.paddleL * 900;

  if (sx === 0) {
    iaMemory.target = Math.floor(Math.random() * 301) + 300;
    if (bx < 600) {
      iaMemory.service = true;
    }
  } else if (sx > 0) {
    iaMemory.target = 450;
  } else {
    while (bx > 60) {
      bx += sx;
      by += sy;
      if (by < 5 || by > 895) {
        sy *= -1;
      }
    }
    iaMemory.target = by + rand;
  }
}

function iaMove () {
  if (iaMemory.pos < iaMemory.target - 10) {
    sendMovement("s");
    iaMemory.pos += iaMemory.step;
  } else if (iaMemory.pos > iaMemory.target + 10) {
    sendMovement("w");
    iaMemory.pos -= iaMemory.step;
  } else if (iaMemory.service) {
    sendMovement("space");
    iaMemory.service = false;
  }
}
// the end of ia town

function receive_data (e) {
  const data = JSON.parse(e.data);
  const endGameScreen = document.getElementById("endGameScreen");
  const endGameMessage = document.getElementById("endGameMessage");
  const confirmEndGame = document.getElementById("confirmEndGame");

  if (data.message === "User exited") {
    endGameMessage.textContent = "The opponent ran away in fear!";
    endGameScreen.style.display = "flex";
    confirmEndGame.onclick = function () {
      gameSocket.send(JSON.stringify({ message: "stop" }));
    };
  }

  if (data.message === "Game stopped") {
    document.getElementById("MyCanvas").hidden = true;
    endGameMessage.textContent = "Game stopped!";
    endGameScreen.style.display = "flex";
    confirmEndGame.onclick = function () {
      gameCanvas.inGame = false;
      gameSocket.close();
      loadPage(ROUTE.GAME_MODES);
      endGameScreen.style.display = "none";
    };
  }

  if (data.message === "win") {
    document.getElementById("MyCanvas").hidden = true;
    endGameMessage.textContent = "You won!";
    endGameScreen.style.display = "flex";
    confirmEndGame.onclick = function () {
      gameCanvas.inGame = false;
      gameSocket.close();
      loadPage(ROUTE.GAME_MODES);
      endGameScreen.style.display = "none";
    };
  }

  if (data.message === "lose") {
    document.getElementById("MyCanvas").hidden = true;
    endGameMessage.textContent = "You lost!";
    endGameScreen.style.display = "flex";
    confirmEndGame.onclick = function () {
      gameCanvas.inGame = false;
      gameSocket.close();
      loadPage(ROUTE.GAME_MODES);
      endGameScreen.style.display = "none";
    };
  }

  if (data.message === "game_finish") {
    document.getElementById("MyCanvas").hidden = true;
    endGameMessage.textContent = data.winner + " won!";
    endGameScreen.style.display = "flex";
    confirmEndGame.onclick = function () {
      gameCanvas.inGame = false;
      gameSocket.close();
      loadPage(ROUTE.GAME_MODES);
      endGameScreen.style.display = "none";
    };
  }

  if (data.message === "opponent") {
    gameCanvas.opponent = data.opponent;
    gameCanvas.num = data.num;
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
    if (GameParams.opponent === "ai" && data.time % 240 === 0) {
      iaBrain(data);
    }
    draw(data);
  }
}

function sendMovement (direction) {
  gameSocket.send(JSON.stringify({ message: direction }));
}

// Fonction pour mettre à jour le mouvement en fonction du temps écoulé
function update () {
  if (keyStates.ArrowUp) {
    sendMovement("up");
  } else if (keyStates.ArrowDown) {
    sendMovement("down");
  } else if (keyStates[" "]) {
    sendMovement("space");
  }
  if (keyStates.w && GameParams.opponent == "player" && GameParams.type == "local") {
    sendMovement("w");
  } else if (keyStates.s && GameParams.opponent == "player" && GameParams.type == "local") {
    sendMovement("s");
  }
  if (GameParams.opponent === "ai") {
    iaMove();
  }
  // Planifiez la prochaine mise à jour
  if (gameStop !== true) {
    requestAnimationFrame(update);
  }
}
