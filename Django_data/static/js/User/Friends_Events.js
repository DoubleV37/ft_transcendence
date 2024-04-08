function  friends_SetEvents() {
  friendsModal['active'] = true;
  let element = document.getElementById('MyFriends');
  if (element) {
    element.addEventListener('submit', friends_DeleteCallBack);
  }

  element = document.getElementById('Suggestions');
  if (element) {
    element.addEventListener('submit', friends_AddCallBack);
  }

  element = document.getElementById('ModalBackArrow');
  element.addEventListener('click', friends_closeModal);

}

function  friends_DelEvents() {
  friendsModal['active'] = false;
  let element = document.getElementById('MyFriends');
  if (element) {
    element.removeEventListener('submit', friends_DeleteCallBack);
  }

  element = document.getElementById('Suggestions');
  if (element) {
    element.removeEventListener('submit', friends_AddCallBack);
  }
  element = document.getElementById('ModalBackArrow');
  element.removeEventListener('click', friends_closeModal);
}
