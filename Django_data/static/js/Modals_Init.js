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
  avatarModal._element.addEventListener('shown.bs.modal', avatar_SetEvents);
  avatarModal._element.addEventListener('hide.bs.modal', avatar_DelEvents);
}

function  modal_2FaInit() {
  TwofaModal = new bootstrap.Modal(document.getElementById('TwofaModal'), {
    backdrop: 'static',
    keyboard: false,
    focus: true});
  TwofaModal._element.addEventListener('shown.bs.modal', Twofa_SetModalEvents);
}

function  modal_2FaCodeInit() {
  TwofaCodeModal = new bootstrap.Modal(document.getElementById('TwofaCodeModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  TwofaCodeModal._element.addEventListener('shown.bs.modal', signin_SetModalEvents);
}
