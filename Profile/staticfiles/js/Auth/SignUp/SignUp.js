async function signUp() {
  let form = document.getElementById('SIGNUP_Form');
  let formData = new FormData(form);

  try {
      const response = await MakeRequest(`${ROUTE.SIGNUP}`, {
	  method: 'POST',
	  body: formData
      });
      if (response.status == 403) {
	 return false;
      }
      const data = await response.json();

      if (data["success"] === true) {
	return true;
      }
      else {
	SignUp_UpdateErrors(data["error"]);
	form.reset();
	return false;
      }
  }
  catch (err) {
    console.error('SignUp Errors:', err);
    return false;
  }
}

function SignUp_UpdateErrors(errors) {
  let element = document.getElementById('SIGNUP_Errors');
  element.innerHTML = '';
  let returnLine = '';

  if (typeof errors !== 'string') {
    returnLine = '<br>';
  }
  for (let key in errors) {
    element.innerHTML += `${errors[key]}${returnLine}`;
  }
}
