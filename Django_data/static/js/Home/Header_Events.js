function  header_SetEvents() {
  let element = document.getElementById('HEADER_Logo');
  element.addEventListener('click', header_LogoCallback);

  element = document.getElementById('HEADER_NavLogo');
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

  element = document.getElementById('HEADER_NavLogo');
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
  loadPage(`${ROUTE.HOME}`);
}

function  header_SignInCallBack() {
  loadPage(`${ROUTE.SIGNIN}`);
}

function  header_ModProfilCallBack() {
  const offcanvasElement = document.getElementById('offcanvasNavbar');
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
      offcanvas.hide();
  }

  profileModal = new bootstrap.Modal(document.getElementById('ProfileModal'));
  profileModal._element.addEventListener('shown.bs.modal', profile_SetEvents);
}

async function  header_SignOutCallBack() {
  const	response = await SignOut();

  if (response == true) {
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    header_SetEvents();
  }
}
