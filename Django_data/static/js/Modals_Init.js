function  modal_ProfileInit() {
  profileModal = new bootstrap.Modal(document.getElementById('ProfileModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  profileModal._element.addEventListener('shown.bs.modal', profile_SetEvents);
  profileModal._element.addEventListener('hide.bs.modal', profile_DelEvents);
}

function  modal_AvatarInit() {
  avatarModal = new bootstrap.Modal(document.getElementById('AvatarModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  avatarModal._element.addEventListener('shown.bs.modal', settings_SetEvents);
  // avatarModal._element.addEventListener('hide.bs.modal', settings_DelEvents);
}