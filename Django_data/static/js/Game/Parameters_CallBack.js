function updateButtonStates () {
  document.querySelectorAll(".input-box").forEach((inputBox) => {
    const value = parseInt(inputBox.value);
    const minusBtn = inputBox.parentNode.querySelector(".minus");
    const plusBtn = inputBox.parentNode.querySelector(".plus");
    minusBtn.disabled = value <= 1;
    plusBtn.disabled = value >= parseInt(inputBox.max);
  });
}

function decreaseValue () {
  const inputBox = this.parentNode.querySelector(".input-box");
  let value = parseInt(inputBox.value);
  value = isNaN(value) ? 1 : Math.max(value - 1, 1);
  inputBox.value = value;
  updateButtonStates();
  updateValue(inputBox.id, value);
}

function increaseValue () {
  const inputBox = this.parentNode.querySelector(".input-box");
  let value = parseInt(inputBox.value);
  value = isNaN(value) ? 1 : Math.min(value + 1, parseInt(inputBox.max));
  inputBox.value = value;
  updateButtonStates();
  updateValue(inputBox.id, value);
}

function updateValue (id, value) {
  if (id === "Difficulty") {
    GameParams.Difficulty = value;
  } else {
    GameParams.Score = value;
  }
}

function parameters_SelectOpponent (event) {
  element = event.target;
  if (event.target.id === "SELECT_Player") {
    if (GameParams.Opponent !== "player") {
      GameParams.Opponent = "player";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_ai").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  } else {
    if (GameParams.Opponent !== "ai") {
      GameParams.Opponent = "ai";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_Player").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  }
}

function parameters_SetPowerUp (event) {
  if (event.target.checked === true) {
    GameParams.PowerUp = true;
  } else {
    GameParams.PowerUp = false;
  }
}

function parameters_StartGame () {
  const Params = JSON.stringify(GameParams);
  console.log(Params);
}

function parameters_SetPage () {
  if (GameParams.Opponent === "ai") {
    document.getElementById("SELECT_ai")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  } else {
    document.getElementById("SELECT_Player")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  }
  document.getElementById("Difficulty").setAttribute("value", GameParams.Difficulty);
  document.getElementById("Score").setAttribute("value", GameParams.Score);

  if (GameParams.PowerUp === true) {
    document.getElementById("switchCheckLabelTop").checked = true;
  } else {
    document.getElementById("switchCheckLabelTop").checked = false;
  }
}
