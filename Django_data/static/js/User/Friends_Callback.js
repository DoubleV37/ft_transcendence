async function friends_DeleteCallBack (event) {
  event.preventDefault();
  const response = await deleteFriendSubmit(event.target);

  if (response === false) {
    friendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

async function friends_AddCallBack (event) {
  event.preventDefault();
  const response = await addFriendSubmit(event.target);

  if (response === false) {
    friendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

async function friends_ResponseCallBack (event) {
  event.preventDefault();
  const response = await ResponseFriendSubmit(event.target);

  if (response === false) {
    friendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

function friends_closeModal () {
  friendsModal.modal.hide();
}

async function friends_GoToProfile (event) {
  const id = event.target.getAttribute("data-content");

  await changeSection(`${ROUTE.PROFILE}${id}/`, "#ProfileModal");
  await changeSection(`${ROUTE.FRIENDS_PROFILE}${id}/`, "#Friends_Profile");
  friendsModal.modal.hide();
  profileModal.modal.show();
}

function friends_CollapseCallback (event) {
  const target =
    event.target.id === "CollapseFriendList"
      ? document.getElementById("CollapseUserList")
      : document.getElementById("CollapseFriendList");

  if (target.getAttribute("aria-expanded") === "true") {
    target.click();
  }
}
