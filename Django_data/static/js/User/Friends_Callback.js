async function friends_DeleteCallBack(event) {

  event.preventDefault();
  const	response = await deleteFriendSubmit();

  if (response == true) {
    header_DelEvents()
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents()
    await changeSection(`${ROUTE.FRIENDS}`, '#content');

  }
}

async function friends_AddCallBack(event) {
  
  event.preventDefault();
  const	response = await addFriendSubmit();

  if (response == true) {
    header_DelEvents()
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents()
    await changeSection(`${ROUTE.FRIENDS}`, '#content');

  }
}

function  friends_closeModal() {
  friendsModal['modal'].hide();
}