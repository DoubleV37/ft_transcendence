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

function Code_SetModalEvents() {
  let element = document.getElementById('form_2FA');
  element.addEventListener('click', code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.addEventListener('click', cancelcode2FACallBack);
}

function Code_DelModalEvents() {
  let element = document.getElementById('form_2FA');
  element.removeEventListener('submit', code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.removeEventListener('click', cancelcode2FACallBack);
}

function  cancelcode2FACallBack(event) {
  event.preventDefault;
  Code_DelModalEvents();
  TwofaCodeModal.hide();
}

async function	code2FACallBack(event) {
  event.preventDefault();
  restore_message();

  const form2FA = document.getElementById('form_2FA');
  const formSIGNIN = document.getElementById('SIGNIN_Form');

  let CombinedForm = new FormData();

  for (const pair of new FormData(form2FA)) {
    CombinedForm.append(pair[0], pair[1]);
  }
  for (const pair of new FormData(formSIGNIN)) {
    CombinedForm.append(pair[0], pair[1]);
  }

  const	response = await MakeRequest(`${ROUTE.TWOFA_C}`, {
    method: 'POST',
    body: CombinedForm
  });
  const data = await response.json();

  if (data.success == true) {
    let element = document.getElementById('success_2FA');

    element.innerHTML = `2FA authentication succeed.`;
    Code_DelModalEvents();
    signin_DelEvents();
    await sleep(2000);
    TwofaCodeModal.hide();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content'); //add some handler event here
    header_SetEvents();
    loadPage(`${ROUTE.HOME}`);
  }
  else {
    let element = document.getElementById('failure_2FA');

    element.innerHTML = `Error: Wrong code submitted. Please try again.`;
  }
}

async function signin_FormCallBack(event) {
  event.preventDefault();
  const	response = await signIn();

  if (response == true) {
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
