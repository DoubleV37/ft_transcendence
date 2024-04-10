function friends_SetEvents () {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");
  let itemList = modal.querySelector("#FriendList").querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.addEventListener("click", friends_GoToProfile);
    delFriend.addEventListener("submit", friends_DeleteCallBack);
  });

  itemList = modal.querySelector("#UserList").querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.addEventListener("click", friends_GoToProfile);
    delFriend.addEventListener("submit", friends_AddCallBack);
  });
  modal.querySelector("#ModalBackArrow")
    .addEventListener("click", friends_closeModal);
}

function friends_DelEvents () {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");
  let itemList = modal.querySelector("#FriendList").querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.removeEventListener("click", friends_GoToProfile);
    delFriend.removeEventListener("submit", friends_DeleteCallBack);
  });

  itemList = modal.querySelector("#UserList").querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.removeEventListener("click", friends_GoToProfile);
    delFriend.removeEventListener("submit", friends_DeleteCallBack);
  });
  modal.querySelector("#ModalBackArrow")
    .removeEventListener("click", friends_closeModal);
}
