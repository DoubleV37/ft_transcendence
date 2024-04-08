function  friends_SetEvents() {
  friendsModal['active'] = true;
  let element = document.getElementById('MyFriends');
  element.addEventListener('submit', friends_DeleteCallBack);

  element = document.getElementById('Suggestions');
  element.removeEventListener('submit', friends_AddCallBack);

  element = document.getElementById('ModalBackArrow');
  element.addEventListener('click', friends_closeModal);

}

function  friends_DelEvents() {
  friendsModal['active'] = false;
  let element = document.getElementById('MyFriends');
  element.removeEventListener('submit', friends_DeleteCallBack);

  element = document.getElementById('Suggestions');
  element.removeEventListener('submit', friends_AddCallBack);

  element = document.getElementById('ModalBackArrow');
  element.removeEventListener('click', friends_closeModal);
}
