function modes_SetEvents() {
  let element = document.getElementById("SELECT_Player");
  element.addEventListener("click", modes_randomMatchmaking);

  element = document.getElementById("SELECT_ai");
  element.addEventListener("click", modes_playerVSia);

  element = document.getElementById("GAME_Create");
  element.addEventListener("click", modes_CreateGame);

  element = document.getElementById("TRNMT_Create");
  element.addEventListener("click", modes_CreateTournament);

  element = document.getElementById("TRNMT_Continue");
  element.addEventListener("click", modes_ContinueTournament);
}

function modes_DelEvents() {
  let element = document.getElementById("SELECT_Player");
  element.removeEventListener("click", modes_randomMatchmaking);

  element = document.getElementById("SELECT_ai");
  element.removeEventListener("click", modes_playerVSia);

  element = document.getElementById("GAME_Create");
  element.removeEventListener("click", modes_CreateGame);

  element = document.getElementById("TRNMT_Create");
  element.removeEventListener("click", modes_CreateTournament);

  element = document.getElementById("TRNMT_Continue");
  element.removeEventListener("click", modes_ContinueTournament);
}
