function  setHeaderEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.addEventListener('click', HeaderLogoCallback);

  element = document.getElementById('HEADER_NavLogo');
  element.addEventListener('click', HeaderLogoCallback);

  element = document.getElementById('HEADER_Signin');
  element.addEventListener('click', HeaderSignInCallBack);
//  .
//  .
//  .
}

function  delHeaderEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.removeEventListener('click', HeaderLogoCallback);

  element = document.getElementById('HEADER_NavLogo');
  element.removeEventListener('click', HeaderLogoCallback);

  element = document.getElementById('HEADER_Signin');
  element.removeEventListener('click', HeaderSignInCallBack);
}

function  HeaderLogoCallback() {
  loadPage(`${ROUTE.HOME}`);
}

function  HeaderSignInCallBack() {
  loadPage(`${ROUTE.SIGNIN}`);
}
