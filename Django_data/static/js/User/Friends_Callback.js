async function friends_DeleteCallBack (event) {
  event.preventDefault();
  console.log(`target = ${event.target}`);
  //const response = await deleteFriendSubmit(event.target);

}

async function friends_AddCallBack (event) {
  event.preventDefault();
  console.log(`target = ${event.target}`);
  const response = await addFriendSubmit(event.target);
  
}

function friends_closeModal () {
  friendsModal.modal.hide();
}

function friends_GoToProfile (event) {
  const id = event.target.getAttribute("data-content");
  console.log(`id = ${id}`);
  changeSection()
  friendsModal.modal.hide();
}
