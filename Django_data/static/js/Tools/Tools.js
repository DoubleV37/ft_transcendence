function  offcanvas_Hide() {
  const offcanvasElement = document.getElementById('offcanvasNavbar');
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
      offcanvas.hide();
  }
}


