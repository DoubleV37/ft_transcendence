let currentUrl = window.location.pathname;
let observer;

let profileModal = {
  'modal': null,
  'active': false,
};

let avatarModal = {
  'modal': null,
  'active': false,
};
let TwofaModal = {
  'modal': null,
  'active': false,
};

let TwofaCodeModal = {
  'modal': null,
  'active': false,
};

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
