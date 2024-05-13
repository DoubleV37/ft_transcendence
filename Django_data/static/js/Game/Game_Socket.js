
function init_websocket () {
  // Create WebSocket connection.
  gameSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
  };
  gameSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
  };
}

function receive_data (e) {
  const data = JSON.parse(e.data);
  if (data.message === "Game stopped") {
    if (gameCanvas.num === 1) {
      gameSocket.send(JSON.stringify({ message: "stop" }));
    }
    return EndGame("Game Stopped!");
  } else if (data.message === "win") {
    return EndGame("You won!");
  } else if (data.message === "lose") {
    return EndGame("You lost!");
  } else if (data.message === "game_finish" && GameParams.opponent != "ai") {
    return EndGame(`${data.winner} won!`);
  } else if (data.message === "game_finish" && GameParams.opponent === "ai") {
    if (data.winner === "IA") { return EndGame("IA-Ochen won!"); }
    return EndGame("You won!");
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

function update () {
  const currentTime = performance.now();
  const deltaTime = currentTime - lastFrameTime;

  if (gameSocket.readyState === 2 || gameSocket.readyState === 3) {
  	return;
  }

  if (deltaTime >= 1000 / targetFrameRate) {
    if (keyStates.ArrowUp) {
      gameSocket.send(JSON.stringify({ message: "up" }));
    } else if (keyStates.ArrowDown) {
      gameSocket.send(JSON.stringify({ message: "down" }));
    } else if (keyStates[" "]) {
      gameSocket.send(JSON.stringify({ message: "space" }));
    }
    if (keyStates.w && GameParams.opponent == "player" && GameParams.type == "local") {
      gameSocket.send(JSON.stringify({ message: "w" }));
    } else if (keyStates.s && GameParams.opponent == "player" && GameParams.type == "local") {
      gameSocket.send(JSON.stringify({ message: "s" }));
    }
    if (GameParams.opponent === "ai") {
      iaMove();
    }

    lastFrameTime = currentTime;
  }
  if (gameStop !== true) {
    requestAnimationFrame(update);
  }
}

function EndGame (message) {
  const endGameScreen = document.getElementById("endGameScreen");
  const endGameMessage = document.getElementById("endGameMessage");
  const confirmEndGame = document.getElementById("confirmEndGame");
  const endGameImage = document.getElementById("endGameImage");

  if (gameSocket != null) {
    gameSocket.close();
  }

  if (message === "You won!") {
    endGameImage.src = playerVictorySrc;
  } else if (message === "You lost!") {
    endGameImage.src = defeatSrc;
  } else if (message === "Game Stopped!") {
    endGameImage.src = stoppedSrc;
  } else if (message === "IA-Ochen won!") {
    endGameImage.src = aiVictorySrc;
  } else {
    endGameImage.src = playerVictorySrc;
  }

  document.getElementById("MyCanvas").hidden = true;
  endGameMessage.textContent = message;

  endGameScreen.style.opacity = "0";

  const id = setTimeout(() => {
    endGameScreen.style.opacity = "1";
  }, 450);

  endGameScreen.style.display = "flex";
  confirmEndGame.onclick = async function () {
    clearTimeout(id);
    await loadPage(ROUTE.GAME_MODES);
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    header_SetEvents();

    endGameScreen.style.display = "none";
  };
  gameCanvas.inGame = false;
}
