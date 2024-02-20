async function signUp() {
  let form = document.getElementById('SIGNUP_Form');
  let formData = new FormData(form);

  try {
      const response = await fetch(`${ROUTE.SIGNUP}`, {
	  method: 'POST',
	  body: formData
      });
      const data = await response.json();

      if (data["status"] === 'success') {
	return true;
      }
      else {
	console.log('Faut gerer la gestion d\'erreur la...');
	form.reset();
	return false;
      }
  }
  catch (err) {
    console.error('SignUp Errors:', err);
    return false;
  }
}
