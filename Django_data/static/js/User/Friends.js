async function addFriendSubmit (form) {
  const formData = new FormData(form);
  const button = form.querySelector("button");
  formData.append(`${button.getAttribute("name")}`, `${button.getAttribute("value")}`);

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData
    });
    // TODO see with jimmy if it's possible to have a list of pending request
    if (response.status === 403) {
      return false;
    }

    return true;
  } catch (err) {
    console.error("Add Friend ERROR:", err);
    return false;
  }
}

async function deleteFriendSubmit (form) {
  const formData = new FormData(form);
  const button = form.querySelector("button");
  formData.append(`${button.getAttribute("name")}`, `${button.getAttribute("value")}`);

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData
    });

    if (response.status === 403) {
      return false;
    }
    // Erase the friend from the list and add it to the Other User list //
    const id = form.getAttribute("data-id");
    const element = document.getElementById(`Friends_${id}`);
    element.remove();
    // TODO Using id, make a back request to get the other user form with good csrf token to make the move //
    return true;
  } catch (err) {
    console.error("Delete Friend ERROR:", err);
    return false;
  }
}

async function ResponseFriendSubmit (button) {
  const form = button.parentNode;
  const formData = new FormData(form);
  formData.append(`${button.getAttribute("name")}`, `${button.getAttribute("value")}`);

  try {
    const response = await MakeRequest(`${ROUTE.REQUESTS}`, {
      method: "POST",
      body: formData
    });

    if (response.status === 403) {
      return false;
    }
    // remove the user from the request list and add it to the friend list if accepted //
    const id = form.getAttribute("data-id");
    const element = document.getElementById(`Request_${id}`);
    element.remove();
    if (button.getAttribute("data-select") === "accept") {
      // Use id in the request //
      // TODO Make a back request to get the right FriendList form with the good csrf.... //
    }
    return true;
  } catch (err) {
    console.error("Delete Friend ERROR:", err);
    return false;
  }
}
