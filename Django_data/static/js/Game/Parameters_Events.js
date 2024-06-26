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

  element = document.getElementById("SELECT_Local");
  element.addEventListener("click", parameters_SelectType);

  element = document.getElementById("SELECT_Remote");
  element.addEventListener("click", parameters_SelectType);

  element = document.getElementById("StartButton");
  element.addEventListener("click", parameters_StartGame);

  const Switch = document.getElementById("switchCheckLabelTop");
  Switch.onkeyup = function (e) {
    if (e.key === "Enter") {
      e.target.checked = e.target.checked === false;
      if (e.target.checked === true) {
        GameParams.powerup = true;
      } else {
        GameParams.powerup = false;
      }
    }
  };
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

  element = document.getElementById("SELECT_Local");
  element.removeEventListener("click", parameters_SelectType);

  element = document.getElementById("SELECT_Remote");
  element.removeEventListener("click", parameters_SelectType);

  element = document.getElementById("StartButton");
  element.removeEventListener("click", parameters_StartGame);

  GameParams.powerup = document.getElementById("switchCheckLabelTop").checked;
}
