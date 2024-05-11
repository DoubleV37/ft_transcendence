async function signIn() {
  const formData = new FormData(document.getElementById('SIGNIN_Form'));

  try {
    const myData = {
      method: 'POST',
      body: formData
    };

    const response = await MakeRequest(`${ROUTE.SIGNIN}`, myData);

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    if (response.ok) {
      const data = await response.json();

      if (data.success == true) {
	      if (data.Twofa == true) {
	        await changeSection(`${ROUTE.TWOFA_C}`, '#code_2fa', );
	        TwofaCodeModal['modal'].show();
	        return '2fa';
	      } else {
	        return true;
	      }
      } else {
	      SignIn_UpdateErrors(data.error);
	      document.getElementById('SIGNIN_Form').reset();
      }
    } else {
      return false;
    }
  } catch (err) {
    console.error('Sign In:', err);
    return false;
  }
}

function SignIn_UpdateErrors(errors) {
  let element = document.getElementById('SIGNIN_Errors');

  element.innerHTML = `Error: ${errors}`;
}
