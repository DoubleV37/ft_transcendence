function modes_SetEvents() {
  let element = document.getElementById("SELECT_Player");
  element.addEventListener("click", modes_randomMatchmaking);

  element = document.getElementById("SELECT_ai");
  element.addEventListener("click", modes_playerVSia);

  element = document.getElementById("GAME_Join");
  element.addEventListener("click", modes_ChooseGame);

  element = document.getElementById("GAME_Create");
  element.addEventListener("click", modes_CreateGame);

  element = document.getElementById("TRNMT_Join");
  element.addEventListener("click", modes_ChooseTournament);

  element = document.getElementById("TRNMT_Create");
  element.addEventListener("click", modes_CreateTournament);

  element = document.getElementById("MultiTest");
  element.addEventListener("click", MultiTestCallback);
}

function modes_DelEvents() {
  let element = document.getElementById("SELECT_Player");
  element.removeEventListener("click", modes_randomMatchmaking);

  element = document.getElementById("SELECT_ai");
  element.removeEventListener("click", modes_playerVSia);

  element = document.getElementById("GAME_Join");
  element.removeEventListener("click", modes_ChooseGame);

  element = document.getElementById("GAME_Create");
  element.removeEventListener("click", modes_CreateGame);

  element = document.getElementById("TRNMT_Join");
  element.removeEventListener("click", modes_ChooseTournament);

  element = document.getElementById("TRNMT_Create");
  element.removeEventListener("click", modes_CreateTournament);

  element = document.getElementById("MultiTest");
  element.removeEventListener("click", MultiTestCallback);
}
