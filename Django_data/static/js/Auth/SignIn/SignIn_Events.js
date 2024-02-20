function  setSignInEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.addEventListener('submit', signInFormCallBack);

  element = document.querySelector("#SIGNIN_Signup p");
  element.addEventListener('click', signUpButtonCallBack);

  element = document.getElementById('signintest');
  element.addEventListener('click', authBy42CallBack);
  //  .
  //  .
  //  .
}

function  delSignInEvents() {
  let element = document.getElementById('SIGNIN_Form');
  element.removeEventListener('submit', signInFormCallBack);

  element = document.querySelector("#SIGNIN_Signup p");
  element.removeEventListener('click', signUpButtonCallBack);

  element = document.getElementById('signintest');
  element.removeEventListener('click', authBy42CallBack);

}

async function signInFormCallBack(event) {
  event.preventDefault();
  const	response = await signIn();

  if (response == true) {
    delSignInEvents();
    loadPage(`${ROUTE.HOME}`);
  }
}

function  authBy42CallBack() {
  console.log('authBy42CallBack: Do nothing for now');
}

function  signUpButtonCallBack() {
  delSignInEvents();
  loadPage(`${ROUTE.SIGNUP}`);
}
