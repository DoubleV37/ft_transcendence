function  home_SetEvents() {

  let element = document.getElementById('SigninButton');
  element.addEventListener('click', SigninCallBack);

  element = document.getElementById('SignupButton');
  element.addEventListener('click', SignupCallBack);
}

function  home_DelEvents() {

  let element = document.getElementById('SigninButton');
  element.removeEventListener('click', SigninCallBack);

  element = document.getElementById('SignupButton');
  element.removeEventListener('click', SignupCallBack);
}

function  SigninCallBack() {
  loadPage(`${ROUTE.SIGNIN}`);
}

function  SignupCallBack() {
  loadPage(`${ROUTE.SIGNUP}`);
}
