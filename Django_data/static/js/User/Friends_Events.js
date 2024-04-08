function  friends_SetEvents() {

  friendsModal['active'] = true;
  let userList = document.getElementById('FriendList');
  // Je cree une liste de formulaires
  let formList = userList.querySelectorAll('form');
  // Je vais chercher les formulaires particuliers
  formList.forEach((addForm) => {
    console.log(addForm);
    // Ajouter event listeners sur chaque FORM 
});
  
  // let element = document.getElementById('MyFriends');
  // if (element) {
  //   element.addEventListener('submit', friends_DeleteCallBack);
  // }

  // element = document.getElementById('Suggestions');
  // if (element) {
  //   element.addEventListener('submit', friends_AddCallBack);
  // }

  // element = document.getElementById('ModalBackArrow');
  // element.addEventListener('click', friends_closeModal);

}

function  friends_DelEvents() {
  friendsModal['active'] = false;
  // let element = document.getElementById('MyFriends');
  // if (element) {
  //   element.removeEventListener('submit', friends_DeleteCallBack);
  // }

  // element = document.getElementById('Suggestions');
  // if (element) {
  //   element.removeEventListener('submit', friends_AddCallBack);
  // }
  // element = document.getElementById('ModalBackArrow');
  // element.removeEventListener('click', friends_closeModal);
}

function  users_SetEvents() {
  friendsModal['active'] = true;
  let userList = document.getElementById('UserList');
  // Je cree une liste de formulaires
  let formList = userList.querySelectorAll('form');
  // Je vais chercher les formulaires particuliers
  formList.forEach((addForm) => {
    console.log(addForm);
    // Ajouter event listeners sur chaque FORM 
});

}

function  users_DelEvents() {
  friendsModal['active'] = false;

}
