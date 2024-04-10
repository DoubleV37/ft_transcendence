async function friends_DeleteCallBack (event) {
  event.preventDefault();
  console.log(`target = ${event.target}`);
  const response = await deleteFriendSubmit(event.target);

  if (response === false) {
    if (error403 === true) {
      return;
    }
    FriendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

async function friends_AddCallBack (event) {
  event.preventDefault();
  console.log(`target = ${event.target}`);
  const response = await addFriendSubmit(event.target);

  if (response === false) {
    if (error403 === true) {
      return;
    }
    FriendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

async function friends_ResponseCallBack (event) {
  event.preventDefault();
  console.log(`target = ${event.target}`);
  const response = await ResponseFriendSubmit(event.target);

  if (response === false) {
    if (error403 === true) {
      return;
    }
    FriendsModal.modal.hide();
    loadPage(`${ROUTE.HOME}`);
  }
}

function friends_closeModal () {
  friendsModal.modal.hide();
}

async function friends_GoToProfile (event) {
  const id = event.target.getAttribute("data-content");

  await changeSection(`${ROUTE.PROFILE}${id}/`, "#ProfileModal");
  friendsModal.modal.hide();
  profileModal.modal.show();
}
