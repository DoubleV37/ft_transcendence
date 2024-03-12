//  button  //
//  PROFIL_Settings --- Ongoing//
//  PROFIL_Skins  //

//  PROFIL_HISTORY //
//  PROFIL_STATS" //
//  PROFIL_42Account //

function  profile_SetEvents() {
  let element = document.getElementById('PROFIL_Settings');

  element.addEventListener('click', profile_SettingsCallBack);

  element = document.getElementById('ModalBackArrow');
  element.addEventListener('click', profile_closeModal);

  element = document.getElementById('PROFIL_Skins');
  element.addEventListener('click', profile_SkinsCallBack);

  element = document.getElementById('PROFIL_History');
  element.addEventListener('click', profile_HistoryCallBack);

  element = document.getElementById('PROFIL_Stats');
  element.addEventListener('click', profile_StatsCallBack);

  element = document.getElementById('PROFIL_42Account');
  element.addEventListener('click', profile_42AccCallBack);
}

function  profile_DelEvents() {
  let element = document.getElementById('PROFIL_Settings');

  element.removeEventListener('click', profile_SettingsCallBack);

  element = document.getElementById('ModalBackArrow');
  element.removeEventListener('click', profile_closeModal);

  element = document.getElementById('PROFIL_Skins');
  element.removeEventListener('click', profile_SkinsCallBack);

  element = document.getElementById('PROFIL_History');
  element.removeEventListener('click', profile_HistoryCallBack);

  element = document.getElementById('PROFIL_Stats');
  element.removeEventListener('click', profile_StatsCallBack);

  element = document.getElementById('PROFIL_42Account');
  element.removeEventListener('click', profile_42AccCallBack);
}

async function  profile_SettingsCallBack() {
  profileModal.hide();
  try {
    await loadPage(`${ROUTE.SETTINGS}`);
  }
  catch (err) {
    console.log(`error profile_settings: ${err}`);
  }
}

function  profile_closeModal() {
  profileModal.hide();
}

async function  profile_SkinsCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("Skins: Do nothing for now");
}

async function  profile_HistoryCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("History: Do nothing for now");
}

async function  profile_StatsCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("Stats: Do nothing for now");
}

async function  profile_42AccCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("42Acc: Do nothing for now");
}
