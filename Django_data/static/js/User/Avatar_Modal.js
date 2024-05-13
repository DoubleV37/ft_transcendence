function avatar_SetEvents () {
  avatarModal.active = true;
  let element = document.getElementById("AvatarBackArrow");
  element.addEventListener("click", avatar_QuitModal);

  element = document.getElementById("customFileButton");
  element.addEventListener("click", avatar_SelectAvatar);

  element = document.getElementById("submitAvatar");
  element.addEventListener("click", avatar_SubmitAvatar);

  element = document.getElementById("AVATAR_Form");
  element.addEventListener("submit", avatar_FormCallBack);

  // Ajoute un écouteur d'événements 'change' à l'input 'id_avatar'
  element = document.getElementById("id_avatar"); // -> in Avatar form
  element.addEventListener("change", displaySelectedImage);
}

function avatar_PrepHtml () {
  element = document.getElementById("submitAvatar");
  element.disabled = true;
  element.setAttribute("class", "SelectButtonLayout ButtonDark");

  document
    .getElementById("selectedAvatar")
    .setAttribute(
      "src",
      document.getElementById("AVATAR_Change_Pic").getAttribute("src")
    );
}

function avatar_DelEvents () {
  avatarModal.active = false;
  let element = document.getElementById("AvatarBackArrow");
  element.removeEventListener("click", avatar_QuitModal);

  element = document.getElementById("customFileButton");
  element.removeEventListener("click", avatar_SelectAvatar);

  element = document.getElementById("submitAvatar");
  element.removeEventListener("click", avatar_SubmitAvatar);

  element = document.getElementById("AVATAR_Form");
  element.removeEventListener("submit", avatar_FormCallBack);

  // Ajoute un écouteur d'événements 'change' à l'input 'id_avatar'
  element = document.getElementById("id_avatar"); // -> in Avatar form
  element.removeEventListener("change", displaySelectedImage);
  document.getElementById("ErrorAvatar").innerHTML = "";
}

function avatar_QuitModal () {
  avatarModal.modal.hide();
}

function avatar_SubmitAvatar () {
  document.getElementById("avatar_button_hidden").click();
}

function avatar_SelectAvatar () {
  document.getElementById("id_avatar").click();
}

function displaySelectedImage (event) {
  const fileInput = event.target.files;
  const selectedImage = document.getElementById("selectedAvatar");

  if (fileInput.length === 0) {
    return;
  }
  document.getElementById("ErrorAvatar").innerHTML = "";
  document
    .getElementById("selectedAvatar")
    .setAttribute("src", "/avatars/ForbiddenDeletion/default.png");
  if (ValidFileType(fileInput[0]) === false) {
    document.getElementById("submitAvatar").disabled = true;
    document
      .getElementById("submitAvatar")
      .setAttribute("class", "SelectButtonLayout ButtonDark");
    document.getElementById("ErrorAvatar").innerHTML = "File type unsupported.";
    return;
  }
  if (fileInput[0].size > 1000000) { //exceed 1MB
    document.getElementById("submitAvatar").disabled = true;
    document
      .getElementById("submitAvatar")
      .setAttribute("class", "SelectButtonLayout ButtonDark");
    document.getElementById("ErrorAvatar").innerHTML = "File too big. Size max < 1MB";
    return;
  }
  const reader = new FileReader();
  reader.onload = function (e) {
    selectedImage.src = e.target.result;
  };
  reader.readAsDataURL(fileInput[0]);
  document.getElementById("submitAvatar").disabled = false;
  document
    .getElementById("submitAvatar")
    .setAttribute("class", "SelectButtonLayout ButtonNeon");
}

async function avatar_FormCallBack (event) {
  event.preventDefault();
  const response = await avatarSubmit();

  if (response === 403 || response === 404) {
    avatarModal.modal.hide();
  } else if (response === true) {
    avatar_QuitModal();
    header_DelEvents();
    settings_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    header_SetEvents();
    await changeSection(`${ROUTE.SETTINGS}`, "#content");
  }
}
