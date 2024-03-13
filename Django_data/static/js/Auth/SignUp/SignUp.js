async function signUp() {
  let form = document.getElementById('SIGNUP_Form');
  let formData = new FormData(form);

  try {
      const response = await MakeRequest(`${ROUTE.SIGNUP}`, {
	  method: 'POST',
	  body: formData
      });
      const data = await response.json();

      if (data["status"] === 'success') {
	return true;
      }
      else {
	SignUp_UpdateErrors(data["message"]);
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

  for (let key in errors) {
    element.innerHTML += `${errors[key]}<br>`;
  }
}
