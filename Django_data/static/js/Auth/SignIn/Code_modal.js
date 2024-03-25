function signin_SetModalEvents() {
  TwofaCodeModal['active'] = true;
  let element = document.getElementById('form_2FA');
  element.addEventListener('submit', signin_Code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.addEventListener('click', signin_Cancelcode2FACallBack);
}

function signin_DelModalEvents() {
  TwofaCodeModal['active'] = false;
  let element = document.getElementById('form_2FA');
  element.removeEventListener('submit', signin_Code2FACallBack);

  element = document.getElementById('cancel_code2fa');
  element.removeEventListener('click', signin_Cancelcode2FACallBack);
}

function signin_Cancelcode2FACallBack() {
  signin_DelModalEvents();
}

async function	signin_Code2FACallBack(event) {
  event.preventDefault();
  restore_message();
  
  const	response = await confirm_2FA_SignIn();

  if (response == true) {
    TwofaCodeModal['modal'].hide();
    signin_DelEvents();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents();
    loadPage(`${ROUTE.HOME}`);
  }
}

async function	confirm_2FA_SignIn() {
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
    return (true);
  }
  else {
    let element = document.getElementById('failure_2FA');

    element.innerHTML = `Error: Wrong code submitted. Please try again.`;
    return (false);
  }
}
