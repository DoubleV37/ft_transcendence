function  header_SetEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.addEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_NavLogo');
  element.addEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'true') {
    element = document.getElementById('HEADER_Profile');
    element.addEventListener('click', header_UserProfilCallBack);

    element = document.getElementById('HEADER_NavSignOut');
    element.addEventListener('click', header_SignOutCallBack);
  }
  else if (IsAuthenticated === 'false') {
    element = document.getElementById('HEADER_Signin');
    element.addEventListener('click', header_SignInCallBack);
  }
  else {
    console.error(`header_SetEvents: error: ${element} unrecognised`);
  }
//  .
//  .
//  .
}

function  header_DelEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.removeEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_NavLogo');
  element.removeEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'true') {
    element = document.getElementById('HEADER_Profile');
    element.removeEventListener('click', header_UserProfilCallBack);

    element = document.getElementById('HEADER_NavSignOut');
    element.removeEventListener('click', header_SignOutCallBack);
  }
  else if (IsAuthenticated === 'false') {
    element = document.getElementById('HEADER_Signin');
    element.removeEventListener('click', header_SignInCallBack);
  }

  else {
    console.error(`header_DelEvents: error: ${element} unrecognised`);
  }
  //  .
  //  .
  //  .
}

function  header_LogoCallback() {
  loadPage(`${ROUTE.HOME}`);
}

function  header_SignInCallBack() {
  loadPage(`${ROUTE.SIGNIN}`);
}

function  header_UserProfilCallBack() {
  console.log('Integrer la modal je sais pas comment encore');
}

async function  header_SignOutCallBack() {
  const	response = await SignOut();

  if (response == true) {
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents();
  }
}
