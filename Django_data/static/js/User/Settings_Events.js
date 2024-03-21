// BIEN SEPARER EVENEMENTS MODAL ET EVENTS SETTINGS
function  settings_SetEvents() {
  let element = document.getElementById('AVATAR_Change');
  element.addEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AVATAR_Change_Pic');
  element.addEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('NAME_Form');
  element.addEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.addEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.addEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.addEventListener('submit', tname_FormCallBack);

  element = document.getElementById('AVATAR_Delete');
  element.addEventListener('click', del_avatar_FormCallBack);

  element = document.getElementById('switchCheckLabelTop');
  element.addEventListener('click', settings_TwoFaCallBack);
}

function  settings_DelEvents() {
  let element = document.getElementById('AVATAR_Change');
  element.removeEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AVATAR_Change_Pic');
  element.removeEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('NAME_Form');
  element.removeEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.removeEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.removeEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.removeEventListener('submit', tname_FormCallBack);

  element = document.getElementById('AVATAR_Delete');
  element.removeEventListener('click', del_avatar_FormCallBack);

  element = document.getElementById('switchCheckLabelTop');
  element.removeEventListener('click', settings_TwoFaCallBack);
}
