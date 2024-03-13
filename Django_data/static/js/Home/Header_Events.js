function  header_SetEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.addEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'true') {
    element = document.getElementById('HEADER_NavSignOut');
    element.addEventListener('click', header_SignOutCallBack);

    element = document.getElementById('HEADER_NavProfile');
    element.addEventListener('click', header_ModProfilCallBack);

    element = document.getElementById('HEADER_Profile');
    element.addEventListener('click', header_ModProfilCallBack);
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

  element = document.getElementById('HEADER_IsAuth');
  const	IsAuthenticated = element.getAttribute('data-auth');

  if (IsAuthenticated === 'true') {
    element = document.getElementById('HEADER_Profile');
    element.removeEventListener('click', header_ModProfilCallBack);

    element = document.getElementById('HEADER_NavProfile');
    element.removeEventListener('click', header_ModProfilCallBack);

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
  try {
    loadPage(`${ROUTE.HOME}`);
  }
  catch (error) {
    console.log(`Error - header_L: ${error}`);
  }
}

function  header_SignInCallBack() {
  try {
    loadPage(`${ROUTE.SIGNIN}`);
  }
  catch (error) {
    console.log(`Error - header_S: ${error}`);
  }
}

async function  header_ModProfilCallBack() {
  try {
    await changeSection(`${ROUTE.PROFILE}`, '#ProfileModal');
    offcanvas_Hide();
    profileModal.show();
  }
  catch (error) {
    console.log(`Error - header_M: ${error}`);
  }
}

async function  header_SignOutCallBack() {
  try {
    await MakeRequest(`${ROUTE.SIGNOUT}`);

    if (currentUrl == ROUTE.HOME) {
      await changeSection(`${ROUTE.HOME}`, '#content');
    }
    else {
      await loadPage(`${ROUTE.HOME}`);
    }
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents();
  }
  catch (err) {
    console.log(`Error - header_SO: ${error}`);
  }
}
