async function nameSubmit() {

  let myForm = document.getElementById('NAME_Form');
  let myData = settings_JsonForm(myForm);

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, myData);
    let data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	// settings_UpdateErrors(data.errors);
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Name Errors:', err);
    return false;
  }
}

async function mailSubmit() {

  let myForm = document.getElementById('MAIL_Form');
  let myData = settings_JsonForm(myForm);

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, myData);
    let data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	// settings_UpdateErrors(data.errors);
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Email Errors:', err);
    return false;
  }
}

async function passSubmit() {

  let myForm = document.getElementById('PASS_Form');
  let myData = settings_JsonForm(myForm);

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, myData);
    let data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	// settings_UpdateErrors(data.errors);
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Password Errors:', err);
    return false;
  }
}

function settings_JsonForm(myForm) {
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

// function settings_UpdateErrors(errors) {
//   let element = document.getElementById('SIGNIN_Errors');

//   element.innerHTML = `Error: ${errors}`;
// }