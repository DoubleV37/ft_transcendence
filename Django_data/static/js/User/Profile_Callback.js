async function profile_SettingsCallBack () {
  try {
    await loadPage(`${ROUTE.SETTINGS}`);
    profileModal.modal.hide();
    historyprofile = [];
  } catch (err) {
    console.log(`Error - profile_S: ${err}`);
  }
}

function profile_closeModal () {
  profileModal.modal.hide();
  historyProfile = [];
}

async function profile_SkinsCallBack () {
  try {
    await loadPage(`${ROUTE.SKINS}`);
    profileModal.modal.hide();
    historyProfile = [];
  } catch (err) {
    console.log(`Error - profile_S: ${err}`);
  }
}

async function profile_HistoryCallBack () {
  const id = document.getElementById("username").getAttribute("data-id");
  await changeSection(`${ROUTE.GAMELIST}${id}/`, "#GameListHistory");
  const list = document.getElementById("GameListHistory").querySelectorAll("button[class]");

  document.getElementById("ProfilPage").hidden = true;
  document.getElementById("ListHistory").hidden = false;

  const backArrow = document.getElementById("ModalBackArrow");

  backArrow.style.display = "flex";
  backArrow.onclick = function () {
    document.getElementById("ProfilPage").hidden = false;
    document.getElementById("ListHistory").hidden = true;
    backArrow.style.display = "none";
  };
  if (list != null) {
    list.forEach((button) => {
      button.addEventListener("click", goToGameStats);
    });
  }
}

async function goToGameStats (event) {
  console.log(`target = ${event.target}`);
  id = event.target.getAttribute("data-gameId");
  const list = document.getElementById("GameListHistory").querySelectorAll("button");
  if (list != null) {
    list.forEach((button) => {
      button.removeEventListener("click", goToGameStats);
    });
  }
  await loadPage(`${ROUTE.GAMEBOARD}${id}`);
  profileModal.modal.hide();
}

function profile_ReturnToProfile () {
  document.getElementById("ListHistory").hidden = true;
  document.getElementById("ProfilPage").hidden = false;
}

async function profile_StatsCallBack () {
  const id = document.getElementById("username").getAttribute("data-id");

  await loadPage(`${ROUTE.STATS}${id}`);
  profileModal.modal.hide();
}

async function profile_FriendsButtonCallBack (event) {
  event.preventDefault();

  const button = event.submitter;
  const formData = new FormData(event.target);
  const type = event.target.getAttribute("data-type");
  let route;

  if (type === "add" || type === "delete") {
    route = `${ROUTE.FRIENDS}`;
  } else {
    route = `${ROUTE.REQUESTS}`;
  }
  formData.append(
    `${button.getAttribute("name")}`,
    `${button.getAttribute("value")}`
  );

  try {
    const response = await MakeRequest(route, {
      method: "POST",
      body: formData
    });
    if (response.status === 403) {
      return false;
    }
    const data = await response.json();
    if (type === "add") {
      const elem = event.target.querySelector("p");
      elem.innerHTML = `<bold>${data.logs}</bold>`;
      button.disabled = true;
    } else {
      const id = event.target.getAttribute("data-id");
      event.target.removeEventListener("submit", profile_FriendsButtonCallBack);
      await changeSection(`${ROUTE.FRIENDS_PROFILE}${id}/`, "#Friends_Profile");
      const element = document.getElementById("Friends_Profile").querySelector("form");
      element.addEventListener("submit", profile_FriendsButtonCallBack);
    }
    return true;
  } catch (err) {
    console.error("ERROR:", err);
    return false;
  }
}

async function profile_GotoFriends () {
  try {
    profileModal.modal.hide();
    await changeSection(`${ROUTE.FRIENDS}`, "#FriendsModal");
    await changeSection(`${ROUTE.REQUESTS}`, "#RequestList-content");
    friendsModal.modal.show();
  } catch (error) {
    console.log(`Error - header_M: ${error}`);
  }
}
