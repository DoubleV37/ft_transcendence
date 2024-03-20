// BIEN SEPARER EVENEMENTS MODAL ET EVENTS SETTINGS
function  settings_SetEvents() {
  let element = document.getElementById('AVATAR_Change');
  element.addEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AVATAR_Change_Pic');
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
  element.addEventListener('click', avatar_FormCallBack);

  element = document.getElementById('NAME_Form');
  element.addEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.addEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.addEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.addEventListener('submit', tname_FormCallBack);

  element = document.getElementById('AVATAR_Form');
  element.addEventListener('submit', avatar_FormCallBack);

  element = document.getElementById('switchCheckLabelTop');
  element.addEventListener('click', settings_TwoFaCallBack);
}

function  settings_DelEvents() {
  let element = document.getElementById('AVATAR_Change');
  element.removeEventListener('click', settings_ModAvatarCallBack);

  element = document.getElementById('AVATAR_Change_Pic');
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
  element.removeEventListener('click', avatar_FormCallBack);

  element = document.getElementById('NAME_Form');
  element.removeEventListener('submit', name_FormCallBack);

  element = document.getElementById('MAIL_Form');
  element.removeEventListener('submit', mail_FormCallBack);

  element = document.getElementById('PASS_Form');
  element.removeEventListener('submit', pass_FormCallBack);

  element = document.getElementById('TNAME_Form');
  element.removeEventListener('submit', tname_FormCallBack);

  element = document.getElementById('AVATAR_Form');
  element.removeEventListener('submit', avatar_FormCallBack);

  element = document.getElementById('switchCheckLabelTop');
  element.removeEventListener('click', settings_TwoFaCallBack);
}

async function  settings_TwoFaCallBack(event) {
  const	element = event.target;

  if (element.checked == true) {
    let form = document.getElementById('TWOFA_Form');
    let formData = new FormData(form);
    const	response = await MakeRequest(`${ROUTE.TWOFA_E}`, {
      method: 'POST',
      body: formData
    });
    _2faOngoing = true;
    const data = await response.json();

    console.log(`data => ${data.status}`);
    if (data.status == 'continue') {
      await changeSection(`${ROUTE.TWOFA_Q}`, '#TwofaModal');
      await changeSection(`${ROUTE.TWOFA_C}`, '#confirm_2fa');
      TwofaModal.show();
    }
    else {
      // modal.show()
      console.log("2FA - succesfully disabled"); //TODO create the modal in JS a la mano
    }
  }
  else {
    let form = document.getElementById('TWOFA_Form');
    let formData = new FormData(form);
     MakeRequest(`${ROUTE.TWOFA_E}`, {
      method: 'POST',
      body: formData
    });
  }
}

async function name_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await nameSubmit();

  if (response == true) {
    changeSection(`${ROUTE.HEADER}`, '#Header_content');
    changeSection(`${ROUTE.SETTINGS}`, '#content');
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
    header_DelEvents()
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents()
    await loadPage(`${ROUTE.HOME}`);
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

async function avatar_FormCallBack(event) 
{
  event.preventDefault();
  const	response = await avatarSubmit();

  if (response == true) {
    settings_closeModal();
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

function  settings_ModAvatarCallBack() {
  avatarModal.show();
}

function  settings_closeModal() {
  avatarModal.hide();
}
