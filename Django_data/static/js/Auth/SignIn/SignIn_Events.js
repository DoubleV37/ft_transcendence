function  signin_SetEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.addEventListener('submit', signin_FormCallBack);

  element = document.querySelector("#SIGNIN_Signup b");
  element.addEventListener('click', signin_SignUpCallBack);

  element = document.getElementById('SIGNIN_Auth42');
  element.addEventListener('click', signin_auth42CallBack);

  element = document.getElementById('forgot_password');
  element.addEventListener('click', signin_ForgotPasswdCallBack);
  //  .
  //  .
  //  .
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

async function signin_FormCallBack(event) {
  event.preventDefault();
  const	response = await signIn();

  if (response == true) {
    signin_DelEvents();
    header_DelEvents();
    await loadPage(`${ROUTE.HOME}`);
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
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
