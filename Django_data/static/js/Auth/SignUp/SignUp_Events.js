function  signup_SetEvents() {
  let element = document.getElementById('SIGNUP_Form');
  element.addEventListener('submit', signup_FormCallBack);

  element = document.querySelector("#SIGNUP_signin b");
  element.addEventListener('click', signup_SignInCallBack);
}

function  signup_DelEvents() {
  let element = document.getElementById('SIGNUP_Form');
  element.removeEventListener('submit', signup_FormCallBack);

  element = document.querySelector("#SIGNUP_signin b");
  element.removeEventListener('click', signup_SignInCallBack);
}

async function signup_FormCallBack(event) {
  event.preventDefault();
  const	response = await signUp();

  if (response == true) {
    await signup_SignInCallBack();
  }
}

async function signup_SignInCallBack() {
    signup_DelEvents();
    await loadPage(`${ROUTE.SIGNIN}`);
}
