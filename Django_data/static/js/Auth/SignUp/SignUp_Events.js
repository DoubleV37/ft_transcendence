function  setSignUpEvents() {
  let element = document.getElementById('SIGNUP_Form');
  element.addEventListener('submit', signUpFormCallBack);

  //  .
  //  .
  //  .
}

function  delSignUpEvents() {
  let element = document.getElementById('SIGNUP_Form');
  element.removeEventListener('submit', signUpFormCallBack);

  //  .
  //  .
  //  .
}

async function signUpFormCallBack(event) {
  event.preventDefault();
  const	response = await signUp();

  if (response == true) {
    delSignUpEvents();
    loadPage(`${ROUTE.SIGNIN}`);
  }
}
