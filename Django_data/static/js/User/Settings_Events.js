// BIEN SEPARER EVENEMENTS MODAL ET EVENTS SETTINGS

function  settings_SetEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.addEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AvatarBackArrow');
  element.addEventListener('click', settings_closeModal);

  element = document.getElementById('customFileButton');
  element.addEventListener('click', selectAvatar);
  
  // Ajoute un écouteur d'événements 'change' à l'input 'id_avatar'
  element = document.getElementById('id_avatar');
  element.addEventListener('change', displaySelectedImage);

  // Target la soumission de formulaire
  element = document.getElementById('submitAvatar');
  element.addEventListener('click', submitAvatar);

  element = document.getElementById('NAME_Form');
  element.addEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.addEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.addEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.addEventListener('submit', tname_FormCallBack);
}

function  settings_DelEvents() {
  let element = document.getElementById('AVATAR_Change');
    element.removeEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AvatarBackArrow');
  element.removeEventListener('click', settings_closeModal);

  element = document.getElementById('customFileButton');
  element.removeEventListener('click', selectAvatar);
  
  // Ajoute un écouteur d'événements 'change' à l'input 'id_avatar'
  element = document.getElementById('id_avatar');
  element.removeEventListener('change', displaySelectedImage);

  // Target la soumission de formulaire
  element = document.getElementById('submitAvatar');
  element.removeEventListener('click', submitAvatar);

  element = document.getElementById('NAME_Form');
  element.removeEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.removeEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.removeEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.removeEventListener('submit', tname_FormCallBack);
}

async function name_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await nameSubmit();

  if (response == true) {
    changeSection(`${ROUTE.HEADER}`, '#Header_content');
    changeSection(`${ROUTE.SETTINGS}`, '#content');
    console.log("PUTAIN - Cordialement");
  }
}

async function mail_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await mailSubmit();

  if (response == true) {
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    await changeSection(`${ROUTE.SETTINGS}`, '#content');
  }
}

async function pass_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await passSubmit();

  if (response == true) {
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    await changeSection(`${ROUTE.HOME}`, '#content');
  }
}

async function tname_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await tnameSubmit();

  if (response == true) {
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    await changeSection(`${ROUTE.SETTINGS}`, '#content');
  }
}

 function displaySelectedImage(event) 
 {
   const fileInput = event.target;
   const selectedImage = document.getElementById('selectedAvatar');
   
   if (fileInput.files && fileInput.files[0]) 
   {
     const reader = new FileReader();   
     reader.onload = function(e) {
       selectedImage.src = e.target.result;
     };     
     reader.readAsDataURL(fileInput.files[0]);
   }
 }

function selectAvatar() {
  document.getElementById('id_avatar').click();
}

function submitAvatar() {
  document.getElementById('AVATAR_Form').submit();
}