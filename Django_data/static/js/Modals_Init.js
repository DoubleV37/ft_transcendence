function  modal_ProfileInit() {
  profileModal['modal'] = new bootstrap.Modal(document.getElementById('ProfileModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  profileModal['modal']._element.addEventListener('shown.bs.modal', profile_SetEvents);
  profileModal['modal']._element.addEventListener('hide.bs.modal', profile_DelEvents);
}

function  modal_FriendsInit() {
  friendsModal['modal'] = new bootstrap.Modal(document.getElementById('FriendsModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  friendsModal['modal']._element.addEventListener('shown.bs.modal', friends_SetEvents);
  friendsModal['modal']._element.addEventListener('hide.bs.modal', friends_DelEvents);
}

function  modal_AvatarInit() {
  avatarModal['modal'] = new bootstrap.Modal(document.getElementById('AvatarModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  avatarModal['modal']._element.addEventListener('shown.bs.modal', avatar_SetEvents);
  avatarModal['modal']._element.addEventListener('hide.bs.modal', avatar_DelEvents);
}

function  modal_2FaInit() {
  TwofaModal['modal'] = new bootstrap.Modal(document.getElementById('TwofaModal'), {
    backdrop: 'static',
    keyboard: false,
    focus: true});
  TwofaModal['modal']._element.addEventListener('shown.bs.modal', Twofa_SetModalEvents);
  TwofaModal['modal']._element.addEventListener('hide.bs.modal', Twofa_DelModalEvents);
}

function  modal_2FaCodeInit() {
  TwofaCodeModal['modal'] = new bootstrap.Modal(document.getElementById('TwofaCodeModal'), {
    backdrop: true,
    keyboard: true,
    focus: true});
  TwofaCodeModal['modal']._element.addEventListener('shown.bs.modal', signin_SetModalEvents);
  TwofaCodeModal['modal']._element.addEventListener('hide.bs.modal', signin_DelModalEvents);
}
