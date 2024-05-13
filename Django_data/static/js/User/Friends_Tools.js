function friends_CreateNewUserElem (form, id) {
  const newNode = () => {
    const node = document.createElement("li");
    const attr = {
      class: "list-group-item",
      id: `Others_${id}`
    };
    Object.keys(attr).forEach((key) => {
      node.setAttribute(key, attr[key]);
    });
    return node;
  };

  const node = document.getElementById(`Friends_${id}`);

  const name = form.getAttribute("data-name");
  const img = node.querySelector("img").getAttribute("src");
  const newNodeElement = newNode();

  let capitalizedName = name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();

  newNodeElement.innerHTML = `<div class="dropdown">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
        <img class="ProfilePic modal-profilePic" src="${img}"></img>
        ${capitalizedName}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <div id="DoubleButton">
            <button class="SelectButtonLayout dropdownButton ButtonNeon" data-content="${id}">Profile</button>
            <form action="" data-id="${id}" onsubmit="return false;" method="post">
              <input>
              <button class="SelectButtonLayout dropdownButton ButtonNeon" type="submit" name="key" value="add ${capitalizedName}">Add</button>
              <p></p>
            </form>
          </div>
        </li>
      </ul>
    </div>`;
  newNodeElement
    .querySelector("input")
    .replaceWith(form.querySelector("input"));
  return newNodeElement;
}

function friends_CreateNewReqElem (form, id, obj) {
  const newNode = () => {
    const node = document.createElement("li");
    const attr = {
      class: "list-group-item",
      id: `${obj.name}_${id}`
    };
    Object.keys(attr).forEach((key) => {
      node.setAttribute(key, attr[key]);
    });
    return node;
  };

  const node = document.getElementById(`Request_${id}`);

  const name = form.getAttribute("data-name");
  const img = node.querySelector("img").getAttribute("src");
  const newNodeElement = newNode();

  let capitalizedName = name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();

  newNodeElement.innerHTML = `<div class="dropdown">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
        <img class="ProfilePic modal-profilePic" src="${img}"></img>
        ${capitalizedName}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <div id="DoubleButton">
            <button class="SelectButtonLayout dropdownButton ButtonNeon" data-content="${id}">Profile</button>
            <form action="" data-name="${name}" data-id="${id}" onsubmit="return false;" method="post">
              <input>
              <button class="SelectButtonLayout dropdownButton ButtonNeon" type="submit" name="key" value="${obj.type.toLowerCase()} ${capitalizedName}">${obj.type}</button>
              <p></p>
            </form>
          </div>
        </li>
      </ul>
    </div>`;
  newNodeElement
    .querySelector("input")
    .replaceWith(form.querySelector("input"));
  return newNodeElement;
}
