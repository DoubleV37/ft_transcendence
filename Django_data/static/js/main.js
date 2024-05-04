// ----------Run at the load/reload of the website-------------//
document.addEventListener("DOMContentLoaded", launchWebsite);

async function launchWebsite () {
  const targetNode = document.querySelector("#content");

  if (!targetNode) {
    console.error("InitMainPage Error: TargetNode not found");
    return;
  }

  const config = { childList: true, subtree: true };

  await changeSection(`${ROUTE.HEADER}`, "#Header_content");

  modal_ProfileInit();
  modal_FriendsInit();
  modal_2FaCodeInit();
  modal_2FaInit();
  modal_AvatarInit();

  header_SetEvents();
  observer = new MutationObserver(mutationCallBack);
  observer.observe(targetNode, config);
  main_SetFirstsEvents();

  document.removeEventListener("DOMContentLoaded", launchWebsite);

  setInterval(pingServer, 3000);
}

function main_SetFirstsEvents () {
  const element = document.getElementById("titleContent");

  if (!element) {
    return;
  }
  launchSectionHandler(element);
}
// -----------------------------------------------------------//

function mutationCallBack (mutationsList) {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList") {
      const element = document.getElementById("titleContent");

      if (!element) {
        continue;
      }
      launchSectionHandler(element);
    }
  }
}

function launchSectionHandler (element) {
  const elementAttribut = element.getAttribute("data-content");

  try {
    switch (elementAttribut) {
    case "HOME_PAGE":
      home_SetEvents();
      break;
    case "SIGNIN_PAGE":
      signin_SetEvents();
      break;
    case "SIGNUP_PAGE":
      signup_SetEvents();
      break;
    case "SETTINGS":
      settings_SetEvents();
      break;
    case "GAME_MODES":
      modes_SetEvents();
      break;
    case "GAME_PARAMETERS":
      parameters_SetEvents();
      break;
    case "GAME_LOCAL":
      observer.disconnect();
      game_SetEvents("GAME_LOCAL");
      break;
    case "GAME_MATCH":
      observer.disconnect();
      matchmaking_SetEvents();
      break;
    case "GAME_ROOM":
      observer.disconnect();
      game_SetEvents("GAME_ROOM");
      break;
    case "SKINS_PAGE":
      skins_SetEvents();
      break;
    case "GAMEBOARD_PAGE":
      gameboard_SetEvents();
      break;
    default:
      throw new Error(
        `launchSectionHandler: Attribute ${elementAttribut} non recognised`
      );
    }
  } catch (err) {
    console.error("Error: ", err);
  }
}
