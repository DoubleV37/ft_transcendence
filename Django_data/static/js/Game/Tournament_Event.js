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
    .querySelectorAll("#StartButton")
    .forEach((button) => {
      button.addEventListener("click", BeginTournament);
    });
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  minusBtns.forEach((btn) => btn.addEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.addEventListener("click", increaseValue));

  const Swicth = document.getElementById("switchCheckLabelTop");
  Swicth.onkeyup = function (e) {
    if (e.key === "Enter") {
      e.target.checked = e.target.checked === false;
    }
  };
}

function tournament_DelEvents () {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");

  minusBtns.forEach((btn) => btn.removeEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.removeEventListener("click", increaseValue));

  document
    .querySelectorAll("#StartButton")
    .forEach((button) => {
      button.removeEventListener("click", BeginTournament);
    });
}

async function BeginTournament () {
  const inputs = [
    document.getElementById("SetPlayer1").value.trim(),
    document.getElementById("SetPlayer2").value.trim(),
    document.getElementById("SetPlayer3").value.trim(),
    document.getElementById("SetPlayer4").value.trim()
  ];
  if (checkInputs(inputs) === false) {
    return;
  }
  tournament = {};
  setPlayerUsername(inputs);
  setParametersGame();
  setSkins();
  createTournament();
}

async function createTournament () {
  tournament_DelEvents();
  try {
    await changeSection(`${ROUTE.GAME_MATCH}`, "#content");
    document.getElementById("titleContent").setAttribute("data-content", "WAITING");
    document.getElementById("matchmakingText").innerHTML = "Creating tournament...";
    await sleep(1000);
    await loadPage(`${ROUTE.BRACKET_TOURNAMENT}`);
  } catch (err) {
    console.error(err);
  }
}

function setSkins () {
  tournament.ball = document
    .getElementById("ballInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament.back = document
    .getElementById("backgroundInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament.P1.paddle = document
    .getElementById("paddleInner1")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament.P2.paddle = document
    .getElementById("paddleInner2")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament.P3.paddle = document
    .getElementById("paddleInner3")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  tournament.P4.paddle = document
    .getElementById("paddleInner4")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
}

function setParametersGame () {
  tournament.score = document.getElementById("Score").value;
  tournament.powerUp = document.getElementById("switchCheckLabelTop").checked;
}

function setPlayerUsername (inputs) {
  tournament.P1 = {};
  tournament.P2 = {};
  tournament.P3 = {};
  tournament.P4 = {};
  tournament.P1.username = inputs[0];
  tournament.P2.username = inputs[1];
  tournament.P3.username = inputs[2];
  tournament.P4.username = inputs[3];
  tournament.P1.img = "/static/images/Player1.png";
  tournament.P2.img = "/static/images/Player2.png";
  tournament.P3.img = "/static/images/Player3.png";
  tournament.P4.img = "/static/images/Player4.png";
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
    value = inputs[i];
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
    if (!values[inputs[i]]) {
      values[inputs[i]] = true;
    } else {
      return false;
    }
  }
  return true;
}
