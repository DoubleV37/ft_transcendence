function validAndSubmit() {

  let username = document.getElementById('id_username').value;
  let password = document.getElementById('id_password').value;

  console.log("username : " + username);
  console.log("password : " + password);
  let validationErrors = [];

  if (!username.trim()) {
    validationErrors.push('Username cannot be empty.');
  }
  if (!password.trim()) {
    validationErrors.push('Password cannot be empty.');
  }

  let validationErrorsDiv = document.getElementById('validationErrors');
  validationErrorsDiv.innerHTML = validationErrors.join('<br>');

  if (validationErrors.length === 0) {
    let form = document.getElementById('signinForm');
    makeBackendRequest(form);
  }
}

function makeBackendRequest(myForm) {
// Make a POST request to the backend to validate the login credentials
  let formData = new FormData(myForm);
  let formDataJSON = {};

  formData.forEach(function(value, key) {
    formDataJSON[key] = value;
  });

  fetch('/auth/signin/', {
      method: 'POST',
      headers: {
	  'Content-Type': 'application/json',
	  'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
      },
      body: JSON.stringify(formDataJSON),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success == true) {
	let button = document.getElementById('signin');

	clickButton(button);
      }
      else {
	updateFormErrors(data.errors);
	myForm.reset();
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function updateFormErrors(errors) {
  validationErrors.innerHTML = `Error: ${errors}`;
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");

    if (parts.length === 2){
      return parts.pop().split(";").shift();
    }
}
