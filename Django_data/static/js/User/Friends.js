async function addFriendSubmit (form) {
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
    const newElement = () => {
      const newNode = document.createElement("li");
      const node = document.getElementById(`Others_${id}`);
      const name = node.querySelector("#dropdownMenuButton1").innerHTML;
      const img = node.querySelector("img").getAttribute("src");
      const input = form.querySelector("input");
        
      `<li class="others list-group-item" id="Others_${id}">
        <div class="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
            ${name}
            <img class="ProfilePic modal-profilePic" src="${img}"></img>
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li>
              <button data-content="${id}">Profile</button>
              <form action="" data-id="${id}" onsubmit="return false;" method="post">
                ${input}
                <button type="submit" name="key" value="add ${name}">Add</button>
                <p></p>
              </form>
            </li>
          </ul>
        </div>
      </li>`;
    };

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
