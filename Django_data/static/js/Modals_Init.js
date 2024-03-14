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

function  modal_2FaInit() {
  TwofaModal = new bootstrap.Modal(document.getElementById('TwofaModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  TwofaModal._element.addEventListener('shown.bs.modal', Twofa_SetModalEvents);
  // avatarModal._element.addEventListener('hide.bs.modal', settings_DelEvents);
}

async function  settings_TwoFaCallBack() {
  await	changeSection(`${ROUTE.TWOFA_E}`, '#TwofaModal');
  TwofaModal.show();
}

function  settings_ModAvatarCallBack() {
  avatarModal.show();
}

function  settings_closeModal() {
  avatarModal.hide();
}
