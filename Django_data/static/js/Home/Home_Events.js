function  home_SetEvents() {

  let element = document.getElementById('SigninButton');
  element.addEventListener('click', home_SigninCallBack);

  element = document.getElementById('SignupButton');
  element.addEventListener('click', home_SignupCallBack);
}

function  home_DelEvents() {

  let element = document.getElementById('SigninButton');
  element.removeEventListener('click', home_SigninCallBack);

  element = document.getElementById('SignupButton');
  element.removeEventListener('click', home_SignupCallBack);
}

function  home_SigninCallBack() {
  try {
    loadPage(`${ROUTE.SIGNIN}`);
  }
  catch (error) {
    console.log(`Error - home_S: ${error}`);
  }
}

function  home_SignupCallBack() {
  try {
    loadPage(`${ROUTE.SIGNUP}`);
  }
  catch (error) {
    console.log(`Error - home_S: ${error}`);
  }
}
