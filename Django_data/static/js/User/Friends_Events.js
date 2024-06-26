function friends_SetEvents () {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");

  // ----------FriendList -----------//
  let itemList = modal.querySelector("#FriendList-content");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      if (parentNode.getAttribute("id") !== "Friends_Empty") {
        const profileButton = parentNode.querySelector("[data-content]");
        const delFriend = parentNode.querySelector("form");

        profileButton.addEventListener("click", friends_GoToProfile);
        delFriend.addEventListener("submit", friends_DeleteCallBack);
      }
    });
  }

  // ----------User suggestion -----------//
  itemList = modal.querySelector("#UserList-content");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      const profileButton = parentNode.querySelector("[data-content]");
      const delFriend = parentNode.querySelector("form");

      profileButton.addEventListener("click", friends_GoToProfile);
      delFriend.addEventListener("submit", friends_AddCallBack);
    });
  }

  itemList = modal.querySelector("#RequestList-content");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      const profileButton = parentNode.querySelector("[data-content]");
      const buttonRequest = parentNode.querySelectorAll("[data-select]");

      profileButton.addEventListener("click", friends_GoToProfile);
      buttonRequest.forEach((button) => {
        button.addEventListener("click", friends_ResponseCallBack);
      });
    });
  }

  modal
    .querySelector("#ModalCloseWindow")
    .addEventListener("click", friends_closeModal);

  modal.querySelector("#ModalBackArrow").onclick = async function () {
    const userid = document.getElementById("HEADER_IsAuth").getAttribute("data-id");

    try {
      await changeSection(`${ROUTE.PROFILE}${userid}/`, "#ProfileModal");
      friendsModal['modal'].hide();
      profileModal['modal'].show();
    } catch (err) {
      console.error("Error:", err);
    }
  };

  modal.querySelectorAll(".btn.btn-primary").forEach((button) => {
    button.addEventListener("click", friends_CollapseCallback);
  });
}

function friends_DelEvents () {
  friendsModal.active = true;
  const modal = document.getElementById("FriendsModal");

  // ----------FriendList -----------//
  let itemList = modal.querySelector("#FriendList-content");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      if (parentNode.getAttribute("id") !== "Friends_Empty") {
        const profileButton = parentNode.querySelector("[data-content]");
        const delFriend = parentNode.querySelector("form");

        profileButton.removeEventListener("click", friends_GoToProfile);
        delFriend.removeEventListener("submit", friends_DeleteCallBack);
      }
    });
  }

  // ----------User suggestion -----------//
  itemList = modal.querySelector("#UserList");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      const profileButton = parentNode.querySelector("[data-content]");
      const delFriend = parentNode.querySelector("form");

      profileButton.removeEventListener("click", friends_GoToProfile);
      delFriend.removeEventListener("submit", friends_AddCallBack);
    });
  }
  // ----------Request receive -----------//
  itemList = modal.querySelector("#RequestList-content");

  if (itemList.innerHTML !== "") {
    itemList.querySelectorAll(".list-group-item").forEach((parentNode) => {
      const profileButton = parentNode.querySelector("[data-content]");
      const buttonRequest = parentNode.querySelectorAll("[data-select]");

      profileButton.removeEventListener("click", friends_GoToProfile);
      buttonRequest.forEach((button) => {
        button.removeEventListener("click", friends_ResponseCallBack);
      });
    });
  }

  modal
    .querySelector("#ModalCloseWindow")
    .removeEventListener("click", friends_closeModal);

  modal.querySelectorAll(".btn.btn-primary").forEach((button) => {
    button.removeEventListener("click", friends_CollapseCallback);
  });
}
