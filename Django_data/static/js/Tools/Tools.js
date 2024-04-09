function offcanvas_Hide () {
  const offcanvasElement = document.getElementById("offcanvasNavbar");
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
    offcanvas.hide();
  }
}

function del_current_event () {
  const page_name = document
    .getElementById("content")
    .getAttribute("data-content");

  switch (page_name) {
  case "HOME_PAGE":
    home_DelEvents();
    break;
  case "SIGNIN_PAGE":
    signin_DelEvents();
    break;
  case "SIGNUP_PAGE":
    signup_DelEvents();
    break;
  case "SETTINGS":
    settings_DelEvents();
    break;
  default:
    break;
  }
}

function sleep (ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function restore_message (elem_success, elem_failure) {
  let element = document.getElementById(elem_failure);
  element.innerHTML = "";

  element = document.getElementById(elem_success);
  element.innerHTML = "";
}
