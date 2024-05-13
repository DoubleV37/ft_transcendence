async function modes_randomMatchmaking() {
	try {
		GameParams.point_limit = 3;
		GameParams.type = "remote";
		GameParams.opponent = "player";
		GameParams.powerup = false;
		GameParams.difficulty = 5;
		GameParams.type_game = "all";
		await loadPage(`${ROUTE.GAME_MATCH}`);
	} catch (error) {
		console.error("Matchmaking:", error);
	}
}

async function modes_playerVSia () {
  try {
    GameParams.opponent = "ai";
    GameParams.type = "local";
    GameParams.point_limit = 3;
    GameParams.difficulty = 5;
    GameParams.powerup = false;
    await loadPage(`${ROUTE.GAME_LOCAL}`);
  } catch (error) {
		console.error("Matchmaking:", error);
  }
}

function modes_CreateGame () {
  loadPage(`${ROUTE.GAME_PARAMETERS}`);
}

function modes_CreateTournament () {
  loadPage(`${ROUTE.SET_TOURNAMENT}`);
}

function modes_ContinueTournament (event) {
  if (tournament != null) {
    loadPage(`${ROUTE.BRACKET_TOURNAMENT}`);
  } else {
    event.target.setAttribute("class", "MediumButtonLayout right ButtonDark");
    event.target.disabled = true;
  }
}
