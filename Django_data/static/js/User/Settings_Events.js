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