async function  profile_SettingsCallBack() {
  try {
    await loadPage(`${ROUTE.SETTINGS}`);
    profileModal['modal'].hide();
  }
  catch (err) {
    console.log(`Error - profile_S: ${err}`);
  }
}

function  profile_closeModal() {
  profileModal['modal'].hide();
}

async function  profile_SkinsCallBack() {
  console.log("Skins: Do nothing for now");
}

function  profile_HistoryCallBack() {
  document.getElementById("ProfilPage").hidden = true;
  document.getElementById("ListHistory").hidden = false;
}

function profile_ReturnToProfile () {
  document.getElementById("ListHistory").hidden = true;
  document.getElementById("ProfilPage").hidden = false;
}

async function  profile_StatsCallBack() {
  console.log("Stats: Do nothing for now");
}

async function  profile_42AccCallBack() {
  console.log("42Acc: Do nothing for now");
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
      event.target.removeEventListener('submit', profile_FriendsButtonCallBack);
      await changeSection(`${ROUTE.FRIENDS_PROFILE}${id}/`, "#Friends_Profile");
      const element = document.getElementById("Friends_Profile").querySelector("form");
      element.addEventListener('submit', profile_FriendsButtonCallBack);
    }
    return true;
  } catch (err) {
    console.error("ERROR:", err);
    return false;
  }
}

async function profile_GotoFriends () {
  try {
    profileModal['modal'].hide();
    await changeSection(`${ROUTE.FRIENDS}`, "#FriendsModal");
    await changeSection(`${ROUTE.REQUESTS}`, "#RequestList-content");
    friendsModal.modal.show();
  } catch (error) {
    console.log(`Error - header_M: ${error}`);
  }

}
