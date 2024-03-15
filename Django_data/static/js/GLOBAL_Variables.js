let currentUrl = window.location.pathname;
let profileModal = null;
let avatarModal = null;
let observer;

const ROUTE = {
  "HOME":"/",
  "HEADER":"/header",
  "SIGNUP":"/auth/signup/",
  "SIGNIN":"/auth/signin/",
  "SIGNOUT":"/auth/signout/",
  "SETTINGS":"/auth/settings/",
  "PROFILE":"/user/profile/",
  "TWOFA_E":"/2fa/enable/",
  "TWOFA_Q":"/2fa/qrcode/",
  "TWOFA_C":"/2fa/confirm/",
  "JWTREFRESH":"/auth/jwt/refresh/",
};
