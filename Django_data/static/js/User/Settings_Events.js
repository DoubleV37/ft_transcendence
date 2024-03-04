function  settings_SetEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.addEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AvatarBackArrow');
  element.addEventListener('click', settings_closeModal);
}

function  settings_DelEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.removeEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AvatarBackArrow');
  element.removeEventListener('click', settings_closeModal);
}

function  settings_ModAvatarCallBack() {
  avatarModal.show();
}

function  settings_closeModal() {
  avatarModal.hide();
}

document.addEventListener('hidden.bs.modal', function (event) {
  // Vérifiez si l'événement provient de la modale d'avatar
  if (event.target.id === 'AvatarModal') {
     settings_SetEvents();
  }
 });