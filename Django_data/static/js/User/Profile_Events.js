//  button  //
//  PROFIL_Settings --- Ongoing//
//  PROFIL_Skins  //

//  PROFIL_HISTORY //
//  PROFIL_STATS" //
//  PROFIL_42Account //

function  profile_SetEvents() {
  let element = document.getElementById('PROFIL_Settings');

  element.addEventListener('click', profile_SettingsCallBack);

}

function  profile_DelEvents() {
  let element = document.getElementById('PROFIL_Settings');

  element.removeEventListener('click', profile_SettingsCallBack);
}

async function  profile_SettingsCallBack() {
  profileModal.hide();
  loadPage(`${ROUTE.SETTINGS}`);
}
