function tournament_SetEvents () {
  const element = [
    document.getElementById("SetPlayer2"),
    document.getElementById("SetPlayer3"),
    document.getElementById("SetPlayer4")
  ];

  element.forEach((inputElement) => {
    inputElement.onkeyup = function () {
      document.getElementById(
        inputElement.getAttribute("data-target")
      ).innerHTML = inputElement.value;
    };
  });
  document
    .getElementById("StartButton")
    .addEventListener("click", BeginTournament);
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  minusBtns.forEach((btn) => btn.addEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.addEventListener("click", increaseValue));
}

function tournament_DelEvents () {
  document
    .getElementById("StartButton")
    .removeEventListener("click", BeginTournament);
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  minusBtns.forEach((btn) => btn.removeEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.removeEventListener("click", increaseValue));
}

async function BeginTournament () {
  const inputs = [
    document.getElementById("SetPlayer1"),
    document.getElementById("SetPlayer2"),
    document.getElementById("SetPlayer3"),
    document.getElementById("SetPlayer4")
  ];
  if (checkInputs(inputs) === false) {
    return;
  }
  tournament = {};
  setPlayerUsername(inputs);
  setParametersGame();
  setSkins();
  createTournament();
  console.log(tournament);
}

async function createTournament () {
  tournament_DelEvents();
  try {
    await changeSection(`${ROUTE.GAME_MATCH}`, "#content");
    document.getElementById("titleContent").setAttribute("data-content", "WAITING");
    await sleep(2000);
    await loadPage(`${ROUTE.BRACKET_TOURNAMENT}`);

  } catch (err) {
    console.error(err);
  }
}

function setSkins () {
  tournament['ball'] = document
    .getElementById("ballInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament['back'] = document
    .getElementById("backgroundInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament['P1']['paddle'] = document
    .getElementById("paddleInner1")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament['P2']['paddle'] = document
    .getElementById("paddleInner2")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament['P3']['paddle'] = document
    .getElementById("paddleInner3")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament['P4']['paddle'] = document
    .getElementById("paddleInner4")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
}

function setParametersGame () {
  tournament['score'] = document.getElementById("Score").value;
  tournament['powerUp'] = document.getElementById("switchCheckLabelTop").checked;
}

function setPlayerUsername (inputs) {
  tournament['P1'] = {};
  tournament['P2'] = {};
  tournament['P3'] = {};
  tournament['P4'] = {};
  tournament['P1']['username'] = inputs[0].value;
  tournament['P2']['username'] = inputs[1].value;
  tournament['P3']['username'] = inputs[2].value;
  tournament['P4']['username'] = inputs[3].value;
}

function checkInputs (inputs) {
  const error = document.getElementById("ErrorMessage");

  if (areUsernamesEmpty(inputs) === true) {
    error.innerHTML = "Username can't be empty!";
    return false;
  }
  if (areUsernamesUnique(inputs) === false) {
    error.innerHTML = "Username can't be the same!";
    return false;
  }
  const value = document.getElementById("Score").value;
  if (isNaN(value) || value < 1 || value > 10) {
    error.innerHTML = "Score need to be a number between 1 and 10!";
    return false;
  }
  return true;
}

function areUsernamesEmpty (inputs) {
  let value;
  const len = inputs.length;

  for (let i = 0; i < len; i++) {
    value = inputs[i].value.trim();
    if (!value) {
      return true;
    }
  }
  return false;
}

function areUsernamesUnique (inputs) {
  const values = {};
  const len = inputs.length;
  for (let i = 0; i < len; i++) {
    if (!values[inputs[i].value]) {
      values[inputs[i].value] = true;
    } else {
      return false; // Duplicate found
    }
  }
  return true; // All usernames are unique
}
