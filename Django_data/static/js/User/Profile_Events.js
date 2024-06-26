function profile_SetEvents () {
  profileModal.active = true;

  const type = document.getElementById("Profile_Type").getAttribute("data-content");
  let element;

  if (type === "himself") {
    element = document.getElementById("PROFIL_Settings");
    element.addEventListener("click", profile_SettingsCallBack);

    element = document.getElementById("PROFIL_Skins");
    element.addEventListener("click", profile_SkinsCallBack);

    element = document.getElementById("PROFIL_Friends");
    element.addEventListener('click', profile_GotoFriends);
  } else {
    element = document.getElementById("Friends_Profile").querySelector("form");
    element.addEventListener('submit', profile_FriendsButtonCallBack);

    element = document.getElementById("ModalBackArrow");
    element.style.display = "flex";
    element.onclick = profile_GotoFriends;
  }

  element = document.getElementById("PROFIL_History");
  element.addEventListener("click", profile_HistoryCallBack);

  element = document.getElementById("PROFIL_Stats");
  element.addEventListener("click", profile_StatsCallBack);

  element = document.getElementById("ModalCloseWindow");
  element.addEventListener("click", profile_closeModal);

}

function profile_DelEvents () {
  profileModal.active = false;

  const type = document.getElementById("Profile_Type").getAttribute("data-content");
  let element;

  if (type === "himself") {
    element = document.getElementById("PROFIL_Settings");
    element.removeEventListener("click", profile_SettingsCallBack);

    element = document.getElementById("PROFIL_Skins");
    element.removeEventListener("click", profile_SkinsCallBack);

    element = document.getElementById("PROFIL_Friends");
    element.removeEventListener('click', profile_GotoFriends);
  } else {
    element = document.getElementById("Friends_Profile").querySelector("form");
    element.removeEventListener('submit', profile_FriendsButtonCallBack);
  }

  element = document.getElementById("PROFIL_History");
  element.removeEventListener("click", profile_HistoryCallBack);

  element = document.getElementById("PROFIL_Stats");
  element.removeEventListener("click", profile_StatsCallBack);

  element = document.getElementById("ModalCloseWindow");
  element.removeEventListener("click", profile_closeModal);
}
