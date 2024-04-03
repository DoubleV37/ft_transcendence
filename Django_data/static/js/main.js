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
  header_SetEvents();

  modal_ProfileInit();
  modal_2FaCodeInit();
  modal_2FaInit();
  modal_AvatarInit();

  main_SetFirstsEvents();

  observer = new MutationObserver(mutationCallBack);
  observer.observe(targetNode, config);

  document.removeEventListener("DOMContentLoaded", launchWebsite);
}

function main_SetFirstsEvents () {
  const element = document.getElementById("titleContent");

  if (!element) {
    console.log("Fuck it...");
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
    case "GAME_PARAMETERS":
      parameters_SetEvents();
      break;
    default:
      throw new Error(`launchSectionHandler: Attribute ${elementAttribut} non recognised`);
    }
  } catch (err) {
    console.error("Error: ", err);
  }
}
