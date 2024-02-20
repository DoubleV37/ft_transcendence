async function signIn() {

  let myForm = document.getElementById('SIGNIN_Form');
  let myData = SignIn_JsonForm(myForm);

  try {
    let response = await fetch(`${ROUTE.SIGNIN}`, myData);
    let data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	SignIn_UpdateErrors(data.errors);
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('SignIn Errors:', errors);
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
    headers: {
	'Content-Type': 'application/json',
	'X-CSRFToken': Tools_GetCookie('csrftoken'),  // Include CSRF token
    },
    body: JSON.stringify(formDataJSON),
  };
  return myData;
}

function SignIn_UpdateErrors(errors) {
  let element = document.getElementById('SIGNIN_Errors');

  element.innerHTML = `Error: ${errors}`;
}