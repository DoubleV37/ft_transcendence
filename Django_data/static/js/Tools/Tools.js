function Tools_GetCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");

  if (parts.length === 2){
    return parts.pop().split(";").shift();
  }
}

function  offcanvas_Hide() {
  const offcanvasElement = document.getElementById('offcanvasNavbar');
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
      offcanvas.hide();
  }
}
