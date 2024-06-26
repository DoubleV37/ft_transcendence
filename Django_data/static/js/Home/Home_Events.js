function home_SetEvents () {
  let element = document.getElementById("titleContent");
  const IsAuthenticated = element.getAttribute("data-connect");

  if (IsAuthenticated === "false") {
    element = document.getElementById("SigninButton");
    element.addEventListener("click", home_SigninCallBack);

    element = document.getElementById("SignupButton");
    element.addEventListener("click", home_SignupCallBack);
  } else {
    element = document.getElementById("PlayButton");
    element.addEventListener("click", home_PlayCallBack);
  }
}

function home_DelEvents () {
  let element = document.getElementById("titleContent");
  const IsAuthenticated = element.getAttribute("data-connect");

  if (IsAuthenticated === "false") {
    element = document.getElementById("SigninButton");
    element.removeEventListener("click", home_SigninCallBack);

    element = document.getElementById("SignupButton");
    element.removeEventListener("click", home_SignupCallBack);
  } else {
    element = document.getElementById("PlayButton");
    element.removeEventListener("click", home_PlayCallBack);
  }
}

function home_PlayCallBack () {
  try {
    loadPage(`${ROUTE.GAME_MODES}`);
  } catch (error) {
    console.error("Home:", error);
  }
}

function home_SigninCallBack () {
  try {
    loadPage(`${ROUTE.SIGNIN}`);
  } catch (error) {
    console.error("Home:", error);
  }
}

function home_SignupCallBack () {
  try {
    loadPage(`${ROUTE.SIGNUP}`);
  } catch (error) {
    console.error("Home:", error);
  }
}
