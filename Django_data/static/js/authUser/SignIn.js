async function SignIn() {

  if (SignIn_EmptyFields() === true) {
    return ;
  }
  let myForm = document.getElementById('signinForm');
  let myData = SignIn_JsonForm(myForm);

  try {
    let response = await Tools_RequestBackEnd('/auth/signin/', myData);
    let data = await response.json();

    if (data.success == true) {
      showSection('/');
      history.pushState({section: '/'}, '');
    }
    else {
	SignIn_UpdateErrors(data.errors);
	myForm.reset();
    }
  }
  catch (errors) {
    console.error('Error:', errors);
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

function SignIn_EmptyFields() {
  let username = document.getElementById('id_username').value;
  let password = document.getElementById('id_password').value;
  let validationErrorsDiv = document.getElementById('validationErrors');

  let validationErrors = [];
  let flag = false;

  if (!username.trim()) {
    validationErrors.push('Username cannot be empty.');
    flag = true;
  }
  if (!password.trim()) {
    validationErrors.push('Password cannot be empty.');
    flag = true;
  }
  validationErrorsDiv.innerHTML = validationErrors.join('<br>');
  return flag;
}

function SignIn_UpdateErrors(errors) {
  validationErrors.innerHTML = `Error: ${errors}`;
}
