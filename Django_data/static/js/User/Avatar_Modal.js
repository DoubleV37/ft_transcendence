function avatar_SetEvents() {
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

  document
    .getElementById("selectedAvatar")
    .setAttribute(
      "src",
      document.getElementById("AVATAR_Change_Pic").getAttribute("src")
    );
}

function avatar_DelEvents() {
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
}

function avatar_QuitModal() {
  avatarModal.modal.hide();
}

function avatar_SubmitAvatar() {
  document.getElementById("avatar_button_hidden").click();
}

function avatar_SelectAvatar() {
  document.getElementById("id_avatar").click();
}

function displaySelectedImage(event) {
  const fileInput = event.target;
  const selectedImage = document.getElementById("selectedAvatar");

  if (fileInput.files && fileInput.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      selectedImage.src = e.target.result;
    };
    reader.readAsDataURL(fileInput.files[0]);
  }
}

async function avatar_FormCallBack(event) {
  event.preventDefault();
  const response = await avatarSubmit();

  if (response == true) {
    avatar_QuitModal();
    header_DelEvents();
    settings_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    header_SetEvents();
    await changeSection(`${ROUTE.SETTINGS}`, "#content");
  }
}
