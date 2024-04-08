function parameters_SetEvents () {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  parameters_SetPage();

  minusBtns.forEach((btn) => btn.addEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.addEventListener("click", increaseValue));

  let element = document.getElementById("SELECT_Player");
  element.addEventListener("click", parameters_SelectOpponent);

  element = document.getElementById("SELECT_ai");
  element.addEventListener("click", parameters_SelectOpponent);

  element = document.getElementById("StartButton");
  element.addEventListener("click", parameters_StartGame);

  element = document.getElementById("switchCheckLabelTop");
  element.addEventListener("click", parameters_SetPowerUp);
}

function parameters_DelEvents () {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  minusBtns.forEach((btn) => btn.removeEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.removeEventListener("click", increaseValue));

  let element = document.getElementById("SELECT_Player");
  element.removeEventListener("click", parameters_SelectOpponent);

  element = document.getElementById("SELECT_ai");
  element.removeEventListener("click", parameters_SelectOpponent);

  element = document.getElementById("StartButton");
  element.removeEventListener("click", parameters_StartGame);

  element = document.getElementById("switchCheckLabelTop");
  element.removeEventListener("click", parameters_SetPowerUp);
}
