function  home_SetEvents() {
  let element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'false') {
    element = document.getElementById('SigninButton');
    element.addEventListener('click', home_SigninCallBack);

    element = document.getElementById('SignupButton');
    element.addEventListener('click', home_SignupCallBack);
  }
  else {
    element = document.getElementById('PlayButton');
    element.addEventListener('click', home_PlayCallBack);

  }
}

function  home_DelEvents() {
  let element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'false') {
    element = document.getElementById('SigninButton');
    element.removeEventListener('click', home_SigninCallBack);

    element = document.getElementById('SignupButton');
    element.removeEventListener('click', home_SignupCallBack);
  }
  else {
    element = document.getElementById('PlayButton');
    element.removeEventListener('click', home_PlayCallBack);
  }
}

function  home_PlayCallBack() {
  console.log("PlayCallBack : Don nothing for now");
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
