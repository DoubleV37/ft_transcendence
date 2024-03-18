function  signin_SetEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.addEventListener('submit', signin_FormCallBack);

  element = document.querySelector("#SIGNIN_Signup b");
  element.addEventListener('click', signin_SignUpCallBack);

  element = document.getElementById('SIGNIN_Auth42');
  element.addEventListener('click', signin_auth42CallBack);

  element = document.getElementById('forgot_password');
  element.addEventListener('click', signin_ForgotPasswdCallBack);
}

function  signin_DelEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.removeEventListener('submit', signin_FormCallBack);

  element = document.querySelector("#SIGNIN_Signup b");
  element.removeEventListener('click', signin_SignUpCallBack);

  element = document.getElementById('SIGNIN_Auth42');
  element.removeEventListener('click', signin_auth42CallBack);

  element = document.getElementById('forgot_password');
  element.removeEventListener('click', signin_ForgotPasswdCallBack);
}

function signin_SetModalEvents() {
  let element = document.getElementById('form_2FA');
  element.addEventListener('submit', signin_Code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.addEventListener('click', signin_Cancelcode2FACallBack);
}

function signin_DelModalEvents() {
  let element = document.getElementById('form_2FA');
  element.removeEventListener('submit', signin_Code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.removeEventListener('click', signin_Cancelcode2FACallBack);
}

function  signin_Cancelcode2FACallBack(event) {
  event.preventDefault;
  signin_DelModalEvents();
  TwofaCodeModal.hide();
}

async function	signin_Code2FACallBack(event) {
  event.preventDefault();
  restore_message();
  
  const	response = await confirm_2FA_SignIn();

  if (response == true) {
    signin_DelModalEvents();
    signin_DelEvents();
    await sleep(2000);
    TwofaCodeModal.hide();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents();
    loadPage(`${ROUTE.HOME}`);
    _2faSignIn = false;
  }
}

async function signin_FormCallBack(event) {
  event.preventDefault();
  const	response = await signIn();

  if (response === '2fa') {
    return ;
  }
  else if (response == true) {
    signin_DelEvents();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    await loadPage(`${ROUTE.HOME}`);
    header_SetEvents();
  }
}

function  signin_auth42CallBack() {
  console.log('signin_auth42CallBack: Do nothing for now');
}

async function  signin_SignUpCallBack() {
  signin_DelEvents();
  await loadPage(`${ROUTE.SIGNUP}`);
}

function  signin_ForgotPasswdCallBack() {
  console.log('signin_ForgotPasswdCallBack: Do nothing for now');
//  delSignInEvents();
//  loadPage(`${ROUTE.FORGOTPASSWORD}`);
}
