async function signIn() {

  const formData = new FormData(document.getElementById('SIGNIN_Form'));

  try {
    const myData = {
      method: 'POST',
      body: formData
    };

    const response = await MakeRequest(`${ROUTE.SIGNIN}`, myData);

    if (response.ok) {
      const data = await response.json();

      if (data.success == true) {
	if (data.Twofa == true) {
	  _2faSignIn = true;
	  await changeSection(`${ROUTE.TWOFA_C}`, '#code_2fa');
	  TwofaCodeModal.show();
	  return '2fa';
	}
	else {
	  return true;
	}
      }
      else {
	SignIn_UpdateErrors(data.error);
	document.getElementById('SIGNIN_Form').reset();
      }
    }
    else {
      if (response.status == 403) {
	Access_Denied(await response.text());
      }
      return false;
    }
  }
  catch (err) {
    console.error('SignIn Errors:', err);
    return false;
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

function SignIn_UpdateErrors(errors) {
  let element = document.getElementById('SIGNIN_Errors');

  element.innerHTML = `Error: ${errors}`;
}
