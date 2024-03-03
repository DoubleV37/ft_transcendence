function  settings_SetEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.addEventListener('click', settings_ModAvatarCallBack);
}

function  settings_DelEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.removeEventListener('click', settings_ModAvatarCallBack);
}

function  settings_ModAvatarCallBack() {
  avatarModal.show();
}

// function  avatar_SetEvents() {
//   let element = document.getElementById('AVATAR_Change');

//   element.addEventListener('click', profile_SettingsCallBack);
// }

// function  avatar_DelEvents() {
//   let element = document.getElementById('AVATAR_Change');

//   element.removeEventListener('click', profile_SettingsCallBack);
// }

// async function  avatar_SettingsCallBack() {
//   profileModal.hide();
//   await loadPage(`${ROUTE.SETTINGS}`);
// }

// function  avatar_closeModal() {
//   profileModal.hide();
// }