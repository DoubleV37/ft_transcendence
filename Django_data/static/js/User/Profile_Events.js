//  button  //
//  PROFIL_Settings //
//  PROFIL_Skins  //

//  PROFIL_HISTORY //
//  PROFIL_STATS" //
//  PROFIL_42Account //

function  profile_SetEvents() {
  let element = document.getElementById('PROFIL_Settings');
  element.addEventListener('click', profile_SettingsCallBack);

  profileModal._element.addEventListener('hide.bs.modal', modalProfileStop);
}

function  profile_DelEvents() {
  let element = document.getElementById('PROFIL_Settings');
  element.removeEventListener('click', profile_SettingsCallBack);
}

async function  profile_SettingsCallBack() {
  profileModal._element.addEventListener('hidden.bs.modal', profile_LoadSettings);
  profile_DelEvents();
  profileModal.hide();
}

async function	profile_LoadSettings() {
  console.log('Putain de bordel');
  profileModal._element.removeEventListener('hidden.bs.modal', profile_LoadSettings);
  console.log('??????????????????');
  await loadPage(`${ROUTE.SETTINGS}`);
}

function modalProfileStop() {
  console.log('Nique ta mere le JS');
  profile_DelEvents();
  profileModal._element.removeEventListener('hide.bs.modal', modalProfileStop);
}
