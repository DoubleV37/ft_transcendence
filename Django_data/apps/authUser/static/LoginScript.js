function validateAndSubmit(event) {

  event.preventDefault();

  let username = document.getElementById('id_username').value;
  let password = document.getElementById('id_password').value;

  let validationErrors = [];

  if (!username.trim()) {
    validationErrors.push('Username cannot be empty.');
  }
  if (!password.trim()) {
    validationErrors.push('Password cannot be empty.');
  }

  let validationErrorsDiv = document.getElementById('validationErrors');
  validationErrorsDiv.innerHTML = validationErrors.join('<br>');

  if (validationErrors.lengh === 0) {
    const form = document.getElementById('signin');
    let formData = new FormData(form);
    makeBackendRequest(formData, form);
  }
  return false
}

function makeBackendRequest(formData, form) {
// Make a POST request to the backend to validate the login credentials
  fetch('/auth/signin', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
      },
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
      if (data.success == true) {
	let button = document.getElementById('button');

	clickButton(button);
      }
      else {
	updateFormErrors(data.erors);
	form.reset();
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function updateFormErrors(errors) {
  const validationErrors = document.getElementById('validationErrors');

  // Clear previous error messages
  validationErrors.innerHTML = '';

  // Loop through the errors object and display each error message
  for (const field in errors) {
    if (errors.hasOwnProperty(field)) {
      const errorMessages = errors[field];

      // Display each error message for the field
      errorMessages.forEach(errorMessage => {
        const errorDiv = document.createElement('div');
        errorDiv.textContent = `${field}: ${errorMessage}`;
        validationErrors.appendChild(errorDiv);
      });
    }
  }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");

    if (parts.length === 2){
      return parts.pop().split(";").shift();
    }
}
