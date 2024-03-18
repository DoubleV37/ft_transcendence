console.log('Hello motherfucker !');
let currentUrl = window.location.pathname;
let profileModal = null;
let avatarModal = null;
let TwofaModal = null;
let TwofaCodeModal = null;
let observer;
let _2faOngoing = false;
let _2faSignIn = false;

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
