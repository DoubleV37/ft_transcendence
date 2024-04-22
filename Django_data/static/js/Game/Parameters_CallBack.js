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
    GameParams.difficulty = value;
  } else {
    GameParams.point_limit = value;
  }
}

function parameters_SelectOpponent (event) {
  element = event.target;
  if (event.target.id === "SELECT_Player") {
    if (GameParams.opponent !== "player") {
      GameParams.opponent = "player";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_ai").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  } else {
    if (GameParams.opponent !== "ai") {
      GameParams.opponent = "ai";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_Player").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  }
}

function parameters_SelectType (event) {
  element = event.target;
  if (event.target.id === "SELECT_Remote") {
    if (GameParams.type !== "remote") {
      GameParams.type = "remote";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_Local").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  } else {
    if (GameParams.type !== "local") {
      GameParams.type = "local";
      event.target.setAttribute("class", "MediumButtonLayout left ButtonNeon");
      document.getElementById("SELECT_Remote").setAttribute("class", "MediumButtonLayout left ButtonDark");
    }
  }
}

function parameters_SetPowerUp (event) {
  if (event.target.checked === true) {
    GameParams.powerup = true;
  } else {
    GameParams.powerup = false;
  }
}

function parameters_StartGame () {
  if (GameParams.type === "local") {
	loadPage(ROUTE.GAME_LOCAL);
  }
  else {
	loadPage(ROUTE.GAME_MATCH);
  }
  const Params = JSON.stringify(GameParams);
  console.log(Params);
}

function parameters_SetPage () {
  if (GameParams.opponent === "ai") {
    document.getElementById("SELECT_ai")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  } else {
    document.getElementById("SELECT_Player")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  }
  if (GameParams.type === "remote") {
    document.getElementById("SELECT_Remote")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  } else {
    document.getElementById("SELECT_Local")
      .setAttribute("class", "MediumButtonLayout left ButtonNeon");
  }
  document.getElementById("Difficulty").setAttribute("value", GameParams.difficulty);
  document.getElementById("Score").setAttribute("value", GameParams.point_limit);

  if (GameParams.powerup === true) {
    document.getElementById("switchCheckLabelTop").checked = true;
  } else {
    document.getElementById("switchCheckLabelTop").checked = false;
  }
}
