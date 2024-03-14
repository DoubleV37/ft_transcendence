async function signIn() {

  const formData = new FormData(document.getElementById('SIGNIN_Form'));

  try {
    const myData = {
      method: 'POST',
      body: formData
    };

    const response = await MakeRequest(`${ROUTE.SIGNIN}`, myData);

    if (response.ok) {
      return true;
    }
    else {
      if (response.status == 403) {
	Access_Denied(await response.text());
      }
      else {
	const data = await response.text();
	console.log(`response -> {data}`);
	SignIn_UpdateErrors(data);
	document.getElementById('SIGNIN_Form').reset();
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
