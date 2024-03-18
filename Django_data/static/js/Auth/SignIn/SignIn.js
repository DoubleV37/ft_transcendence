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
	  await changeSection(`${ROUTE.TWOFA_C}`, '#code_2fa');
	  TwofaCodeModal.show();
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

function SignIn_JsonForm(myForm) {
  let formData = new FormData(myForm);
  let formDataJSON = {};

  formData.forEach(function(value, key) {
    formDataJSON[key] = value;
  });

  let myData = {
    method: 'POST',
    body: JSON.stringify(formDataJSON),
  };
  return myData;
}

function SignIn_UpdateErrors(errors) {
  let element = document.getElementById('SIGNIN_Errors');

  element.innerHTML = `Error: ${errors}`;
}
