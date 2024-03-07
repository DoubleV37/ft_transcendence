//function Tools_GetCookie(name) {
//  let value = "; " + document.cookie;
//  let parts = value.split("; " + name + "=");
//  console.log(`cookie = ${document.cookie}`);
//  console.log(`value = ${value}`);
//  console.log(`parts = ${parts}`);
//
//  if (parts.length === 2){
//    value = parts.pop().split(";").shift();
//    console.log(`value2 = ${value}`);
//
//    return value;
//  }
//}

function getCookie(name) {
 if (!document.cookie) {
    return null;
 }

 const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

 if (xsrfCookies.length === 0) {
    return null;
 }
 return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

function  offcanvas_Hide() {
  const offcanvasElement = document.getElementById('offcanvasNavbar');
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);

  if (offcanvas) {
      offcanvas.hide();
  }
}
