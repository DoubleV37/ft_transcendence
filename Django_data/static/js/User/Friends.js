async function addFriendSubmit(form) {
  const formData = new FormData(form);
  const button = form.querySelector("button");
  formData.append(
    `${button.getAttribute("name")}`,
    `${button.getAttribute("value")}`
  );

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData,
    });
    if (response.status === 403) {
      return false;
    }
    const data = await response.json();
    const elem = form.querySelector("p");
    elem.innerHTML = `<bold>${data.logs}</bold>`;
    button.disabled = true;
    return true;
  } catch (err) {
    console.error("Add Friend ERROR:", err);
    return false;
  }
}

async function deleteFriendSubmit(form) {
  const formData = new FormData(form);
  const button = form.querySelector("button");
  formData.append(
    `${button.getAttribute("name")}`,
    `${button.getAttribute("value")}`
  );

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData,
    });

    if (response.status === 403) {
      return false;
    }
    const id = form.getAttribute("data-id");

    // Remove Current Event //
    document
      .getElementById(`Friends_${id}`)
      .querySelector("button[data-content]")
      .removeEventListener("click", friends_GoToProfile);
    form.removeEventListener("submit", deleteFriendSubmit);

    // Erase the friend from the list and add it to the Other User list //
    const newListElement = friends_CreateNewUserElem(form, id);
    document
      .getElementById("UserList-content")
      .append(newListElement);
    document.getElementById(`Friends_${id}`).remove();
    const newForm = newListElement.querySelector("form");
    const newButton = newListElement.querySelector("button[data-content]");
    newForm.addEventListener("submit", friends_AddCallBack);
    newButton.addEventListener("click", friends_GoToProfile);
    if (document.getElementById("FriendList-content").querySelectorAll(".list-group-item").length === 1) {
      document.getElementById("Friends_Empty").hidden = false;
    }
    return true;
  } catch (err) {
    console.error("Delete Friend ERROR:", err);
    return false;
  }
}

async function ResponseFriendSubmit(button) {
  const form = button.parentNode;
  const formData = new FormData(form);
  formData.append(
    `${button.getAttribute("name")}`,
    `${button.getAttribute("value")}`
  );

  try {
    const response = await MakeRequest(`${ROUTE.REQUESTS}`, {
      method: "POST",
      body: formData,
    });

    if (response.status === 403) {
      return false;
    }
    const id = form.getAttribute("data-id");

    // remove the eventslistener
    document
      .getElementById(`Request_${id}`)
      .querySelector("button[data-content]")
      .removeEventListener("click", friends_GoToProfile);
    form.querySelectorAll("button").forEach((button) => {
      button.removeEventListener("click", ResponseFriendSubmit);
    });

    // remove the user from the request list and add it to the friend list if accepted //
    const type = button.getAttribute("data-select");
    const func =
      type === "accept" ? friends_DeleteCallBack : friends_AddCallBack;
    const list = type === "accept" ? "FriendList-content" : "UserList-content";
    const obj =
      type === "accept"
        ? { name: "Friends", type: "Delete" }
        : { name: "Others", type: "Add" };

    const newListElement = friends_CreateNewReqElem(form, id, obj);
    document
      .getElementById(list)
      .append(newListElement);
    document.getElementById(`Request_${id}`).remove();
    const newForm = newListElement.querySelector("form");
    const newButton = newListElement.querySelector("button[data-content]");

    newForm.addEventListener("submit", func);
    newButton.addEventListener("click", friends_GoToProfile);
    if (document.getElementById("FriendList-content").querySelectorAll(".list-group-item").length > 1) {
      document.getElementById("Friends_Empty").hidden = true;
    }
    return true;
  } catch (err) {
    console.error("Delete Friend ERROR:", err);
    return false;
  }
}
