function offcanvas_Hide () {
  const offcanvasElement = document.getElementById("offcanvasNavbar");
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
    offcanvas.hide();
  }
}

function del_current_event () {
  const page_name = document
    .getElementById("titleContent")
    .getAttribute("data-content");

  switch (page_name) {
  case "HOME_PAGE":
    home_DelEvents();
    break;
  case "SIGNIN_PAGE":
    signin_DelEvents();
    break;
  case "SIGNUP_PAGE":
    signup_DelEvents();
    break;
  case "SETTINGS":
    settings_DelEvents();
    break;
  case "GAME_MODES":
    modes_DelEvents();
    break;
  case "SKINS_PAGE":
    skins_DelEvents();
    break;
  case "GAME_PARAMETERS":
    parameters_DelEvents();
    break;
  case "GAME_LOCAL":
    game_DelEvents();
    break;
  case "GAME_MATCH":
    matchmaking_DelEvents();
    break;
  case "GAME_ROOM":
    game_DelEvents();
    break;
  default:
    break;
  }
}

function sleep (ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function restore_message (elem_success, elem_failure) {
  let element = document.getElementById(elem_failure);
  element.innerHTML = "";

  element = document.getElementById(elem_success);
  element.innerHTML = "";
}

async function pingServer () {
  try {
    const response = await fetch(`${ROUTE.PING}`, {
      method: "POST",
      headers: {
        "Content-Length": 0
      }
    });

    if (!response.ok) {
      throw new Error(`Network response: ${response.ok}`);
    }
  } catch (error) {
    console.error("Error: ", error);
  }
}
