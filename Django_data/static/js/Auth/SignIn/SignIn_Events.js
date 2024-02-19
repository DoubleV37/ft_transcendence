function  setSignInEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.addEventListener('submit', signInFormCallBack);

  element = document.getElementById('SIGNIN_Signup');
  element.addEventListener('click', signUpButtonCallBack);
  //  .
  //  .
  //  .
}

function  delSignInEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.removeEventListener('submit', signInFormCallBack);

  element = document.getElementById('SIGNIN_Signup');
  element.removeEventListener('click', signUpButtonCallBack);

}

async function signInFormCallBack(event) {
  event.preventDefault();
  const	response = await signIn();

  if (response == true) {
    delSignInEvents();
    loadPage(`${ROUTE.HOME}`);
  }
}

function  signUpButtonCallBack() {
  delSignInEvents();
  loadPage(`${ROUTE.SIGNUP}`);
}
