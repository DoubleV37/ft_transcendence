function SignIn() {

  if (SignIn_EmptyFields() === true) {
    return ;
  }
//  let username = document.getElementById('id_username').value;
//  let password = document.getElementById('id_password').value;
//
//  let validationErrors = [];
//
//  if (!username.trim()) {
//    validationErrors.push('Username cannot be empty.');
//  }
//  if (!password.trim()) {
//    validationErrors.push('Password cannot be empty.');
//  }
//
//  let validationErrorsDiv = document.getElementById('validationErrors');
//  validationErrorsDiv.innerHTML = validationErrors.join('<br>');

  let myForm = document.getElementById('signinForm');
  let formData = new FormData(myForm);
  let formDataJSON = {};

  formData.forEach(function(value, key) {
    formDataJSON[key] = value;
  });

  //makeBackendRequest(form);

  let myData = {
    method: 'POST',
    headers: {
	'Content-Type': 'application/json',
	'X-CSRFToken': Tools_GetCookie('csrftoken'),  // Include CSRF token
    },
    body: JSON.stringify(formDataJSON),
  };

  Tools_RequestBackEnd('/auth/signin/', myData)
  .then(data => {
    if (data.success == true) {
      let button = document.getElementById('signin');

      clickButton(button);
    }
    else {
      SignIn_UpdateErrors(data.errors);
      myForm.reset();
    }
  });
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

//function makeBackendRequest(myForm) {
//// Make a POST request to the backend to validate the login credentials
//  let formData = new FormData(myForm);
//  let formDataJSON = {};
//
//  formData.forEach(function(value, key) {
//    formDataJSON[key] = value;
//  });
//
//  fetch('/auth/signin/', {
//      method: 'POST',
//      headers: {
//	  'Content-Type': 'application/json',
//	  'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
//      },
//      body: JSON.stringify(formDataJSON),
//  })
//  .then(response => response.json())
//  .then(data => {
//      if (data.success == true) {
//	let button = document.getElementById('signin');
//
//	clickButton(button);
//      }
//      else {
//	updateFormErrors(data.errors);
//	myForm.reset();
//      }
//  })
//  .catch(error => {
//      console.error('Error:', error);
//  });
//}


// Function to get CSRF token from cookies
//function getCookie(name) {
//    var value = "; " + document.cookie;
//    var parts = value.split("; " + name + "=");
//
//    if (parts.length === 2){
//      return parts.pop().split(";").shift();
//    }
//}
