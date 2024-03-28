function  profile_SetEvents() {
  profileModal['active'] = true;
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
  profileModal['active'] = false;
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
