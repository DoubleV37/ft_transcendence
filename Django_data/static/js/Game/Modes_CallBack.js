async function modes_randomMatchmaking() {
	try {
		await loadPage(`${ROUTE.GAME_MATCH}`);
	} catch (error) {
		console.log(`Error - playerVSplayer: ${error}`);
	}
}

async function modes_playerVSia() {
	try {
		await loadPage(`${ROUTE.GAME_SOLO}`);
	} catch (error) {
		console.log(`Error - playerVSia: ${error}`);
	}
}

function modes_ChooseGame() {
  console.log("ChooseGame: do nothing for now");
}

async function modes_CreateGame() {
  await loadPage(`${ROUTE.GAME_PARAMETERS}`);
}

function modes_ChooseTournament() {
  console.log("ChooseTournament: do nothing for now");
}

function modes_CreateTournament() {
  console.log("CreateTournament: do nothing for now");
}
