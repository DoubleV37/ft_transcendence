function bracket_SetEvents() {
  setTournamentState();
}

async function setTournamentState() {
  if (tournament === null || tournament === undefined) {
    await loadPage(`${ROUTE.SET_TOURNAMENT}`);
  } else {
    updateBracket();
  }
}

function updateBracket() {
  PlayerList = [tournament.P1, tournament.P2, tournament.P3, tournament.P4];

  if (isNotSet(PlayerList) === true) {
    setMatchInfo();
  }
  setRound();
  console.log(tournament);
}

function setRounds() {
  const players = [tournament.P1, tournament.P2, tournament.P3, tournament.P4];

  players.forEach((player) => {
    const element = document.querySelector(`div[data-match=${player.match}]`);
    if ("winner" in player) {
      player.winner
        ? element.setAttribute("class", "team-winner")
        : element.setAttribute("class", "team-loser");
    }

  });
}

function setMatchInfo() {
  const players = shufflePlayer(["P1", "P2", "P3", "P4"]);
  const match = shufflePlayer([1, 2]);

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

function shufflePlayer(list) {
  let j;

  for (let i = list.length - 1; i > 0; i--) {
    j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }
  console.log(list);
  return list;
}

function isNotSet(playerList) {
  const len = playerList.length;

  for (let i = 0; i < len; i++) {
    if ("vs" in playerList[i]) {
      return false;
    }
  }
  return true;
}
