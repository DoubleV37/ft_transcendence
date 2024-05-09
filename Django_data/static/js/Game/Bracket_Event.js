async function bracket_SetEvents () {
  if (tournament === null || tournament === undefined) {
    await loadPage(`${ROUTE.SET_TOURNAMENT}`);
  } else {
    updateBracket();
  }
}

function bracket_DelEvents () {
  if (document.getElementById("Bracket").hidden === true) {
    if (gameSocket.readyState === WebSocket.OPEN ||
        gameSocket.readyState === WebSocket.CONNECTING) { gameSocket.close(); }
  }
}

function updateBracket () {
  playerList = [tournament.P1, tournament.P2, tournament.P3, tournament.P4];

  if (isNotSet(playerList) === true) {
    setMatchInfo();
  }
  setRounds();
  const button = document.getElementById("PlayButton");
  if ("winner" in tournament) {
    endTournament(tournament.winner);
  } else {
    button.querySelector("span").innerHTML = "Launch next round!";
    button.onclick = () => {
      const players = whichPlayer(playerList);
      setGame(players);
      launchGame();
    };
  }
}

function endTournament (winner) {
  const Screen = document.getElementById("endTournamentScreen");
  const Message = document.getElementById("endTournamentMessage");
  const Confirm = document.getElementById("confirmEndTournament");

  document.getElementById("sectionTournament").hidden = true;
  Confirm.innerHTML = "Leave tournament";
  Message.textContent = `${winner} won the tournament!`;
  Screen.style.display = "flex";
  Confirm.onclick = function () {
    Screen.style.display = "none";
    loadPage(`${ROUTE.SET_TOURNAMENT}`);
    tournament = null;
  };
}

function setGameInfo (players) {
  document
    .getElementById("MyCanvas")
    .setAttribute("style", `background: url('${tournament.back}')`);
  GameInfos.Ball.img = new Image();
  GameInfos.Ball.img.onload = () => {
    const rightName = document.getElementById("GAME_username_right");
    const leftName = document.getElementById("GAME_username_left");

    if (players[0].team === 1) {
      rightName.innerHTML = players[0].vs;
      leftName.innerHTML = players[0].username;
      GameInfos.PlayerR.srcPaddle = players[0].paddle;
      GameInfos.PlayerR.username = players[0].username;
      GameInfos.PlayerL.srcPaddle = players[1].paddle;
      GameInfos.PlayerL.username = players[1].username;
    } else {
      rightName.innerHTML = players[0].username;
      leftName.innerHTML = players[0].vs;
      GameInfos.PlayerL.srcPaddle = players[0].paddle;
      GameInfos.PlayerL.username = players[0].username;
      GameInfos.PlayerR.srcPaddle = players[1].paddle;
      GameInfos.PlayerR.username = players[1].username;
    }
    GameInfos.PlayerR.canvas = initRotatedImage(
      GameInfos.PlayerR.srcPaddle,
      false
    );
    GameInfos.PlayerL.canvas = initRotatedImage(
      GameInfos.PlayerL.srcPaddle,
      true
    );
  };
  GameInfos.Ball.img.src = tournament.ball;
  GameParams.opponent = "player";
  GameParams.type = "local";
  GameParams.point_limit = parseInt(tournament.score);
  GameParams.powerup = tournament.powerUp;
  GameParams.type_game = "tournament";
  gameCanvas.powerup = GameParams.powerup;
}

function whichPlayer (playerList) {
  const len = playerList.length;
  const players = [];

  for (let i = 0; i < len; i++) {
    if (playerList[i].match === tournament.match) {
      players.push(playerList[i]);
    }
  }
  return players;
}

function setRounds () {
  const players = [tournament.P1, tournament.P2, tournament.P3, tournament.P4];

  players.forEach((player) => {
    const element = document.querySelector(`div[data-match="${player.match}"]`);
    setPlayer(player, element);
    setOpponent(player, element);
  });
}

function setOpponent (player, match) {
  const team =
    player.team === 1
      ? match.querySelector("div[data-team=\"2\"]")
      : match.querySelector("div[data-team=\"1\"]");
  if ("winner" in player) {
    player.winner
      ? team.setAttribute("class", "team-loser")
      : player.round === 3
        ? team.setAttribute("class", "winner")
        : team.setAttribute("class", "team-winner");
  }
  if (player.vs !== "") {
    team.querySelector("span").innerHTML = player.vs;
  }
}

function setPlayer (player, match) {
  const team = match.querySelector(`div[data-team="${player.team}"]`);
  if ("winner" in player) {
    !player.winner
      ? team.setAttribute("class", "team-loser")
      : player.round === 3
        ? team.setAttribute("class", "winner")
        : team.setAttribute("class", "team-winner");
  }
  team.querySelector("span").innerHTML = player.username;
}

function setMatchInfo () {
  const players = shufflePlayer(["P1", "P2", "P3", "P4"]);
  const match = shufflePlayer([1, 2]);

  tournament.match = 1;
  tournament[players[0]].vs = tournament[players[1]].username;
  tournament[players[0]].match = match[0];
  tournament[players[0]].round = 1;
  tournament[players[0]].team = 1;
  tournament[players[1]].vs = tournament[players[0]].username;
  tournament[players[1]].match = match[0];
  tournament[players[1]].round = 1;
  tournament[players[1]].team = 2;
  tournament[players[2]].vs = tournament[players[3]].username;
  tournament[players[2]].match = match[1];
  tournament[players[2]].round = 1;
  tournament[players[2]].team = 1;
  tournament[players[3]].vs = tournament[players[2]].username;
  tournament[players[3]].match = match[1];
  tournament[players[3]].round = 1;
  tournament[players[3]].team = 2;
}

function shufflePlayer (list) {
  let j;

  for (let i = list.length - 1; i > 0; i--) {
    j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }
  return list;
}

function isNotSet (playerList) {
  const len = playerList.length;

  for (let i = 0; i < len; i++) {
    if ("vs" in playerList[i]) {
      return false;
    }
  }
  return true;
}
