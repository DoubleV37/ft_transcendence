function friends_SetEvents() {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");

  // ----------FriendList -----------//
  let itemList = modal
    .querySelector("#FriendList-content")
    .querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.addEventListener("click", friends_GoToProfile);
    delFriend.addEventListener("submit", friends_DeleteCallBack);
  });

  // ----------User suggestion -----------//
  itemList = modal
    .querySelector("#UserList")
    .querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.addEventListener("click", friends_GoToProfile);
    delFriend.addEventListener("submit", friends_AddCallBack);
  });

  // ----------Request receive -----------//
  if (
    modal
      .querySelector("#RequestList-content")
      .querySelector(".list-group")
      .innerHTML.trim() === ""
  ) {
    modal.querySelector("#RequestList-content").querySelector("p").innerHTML =
      "";
  }

  itemList = modal
    .querySelector("#RequestList-content")
    .querySelectorAll(".list-group-item");
  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const buttonRequest = parentNode.querySelectorAll("[data-select]");

    profileButton.addEventListener("click", friends_GoToProfile);
    buttonRequest.forEach((button) => {
      button.addEventListener("click", friends_ResponseCallBack);
    });
  });

  modal
    .querySelector("#ModalBackArrow")
    .addEventListener("click", friends_closeModal);

  modal.querySelectorAll(".btn.btn-primary").forEach((button) => {
    button.addEventListener("click", friends_CollapseCallback);
  });
  modal.querySelector("#CollapseFriendList").click();
}

function friends_DelEvents() {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");

  // ----------FriendList -----------//
  let itemList = modal
    .querySelector("#FriendList-content")
    .querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.removeEventListener("click", friends_GoToProfile);
    delFriend.removeEventListener("submit", friends_DeleteCallBack);
  });

  // ----------User suggestion -----------//
  itemList = modal
    .querySelector("#UserList")
    .querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const delFriend = parentNode.querySelector("form");

    profileButton.removeEventListener("click", friends_GoToProfile);
    delFriend.removeEventListener("submit", friends_AddCallBack);
  });

  // ----------Request receive -----------//
  itemList = modal
    .querySelector("#RequestList-content")
    .querySelectorAll(".list-group-item");

  itemList.forEach((parentNode) => {
    const profileButton = parentNode.querySelector("[data-content]");
    const buttonRequest = parentNode.querySelectorAll("[data-select]");

    profileButton.removeEventListener("click", friends_GoToProfile);
    buttonRequest.forEach((button) => {
      button.removeEventListener("click", friends_ResponseCallBack);
    });
  });

  modal
    .querySelector("#ModalBackArrow")
    .removeEventListener("click", friends_closeModal);

  modal.querySelectorAll(".btn.btn-primary").forEach((button) => {
    button.removeEventListener("click", friends_CollapseCallback);
  });
}
