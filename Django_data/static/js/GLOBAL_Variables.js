let currentUrl = window.location.pathname;
let observer;
let _2faSignIn = false;

let error403 = false;

let profileModal = {
  modal: null,
  active: false
};

let avatarModal = {
  modal: null,
  active: false
};
let TwofaModal = {
  modal: null,
  active: false
};

let TwofaCodeModal = {
  modal: null,
  active: false
};

let GameParams = {
  Opponent: "ai",
  Type: "local",
  Score: 3,
  Difficulty: 5,
  PowerUp: false
};

const ROUTE = {
  HOME: "/",
  HEADER: "/header",
  FOOTER: "/footer",
  SIGNUP: "/auth/signup/",
  SIGNIN: "/auth/signin/",
  SIGNOUT: "/auth/signout/",
  SETTINGS: "/auth/settings/",
  PROFILE: "/user/profile/",
  TWOFA_E: "/2fa/enable/",
  TWOFA_Q: "/2fa/qrcode/",
  TWOFA_C: "/2fa/confirm/",
  JWTREFRESH: "/auth/jwt/refresh/",
  GAME_PARAMETERS: "/game/parameters/",
  GAME_MODES: "/game/modes/",
  GAME_SOLO: "/game/solo/",
//   "GAME_ROOM":"/game/", //`${ROUTE.GAME_ROOM}${id...}/`
};

// INIT POWERUP
let imgPowerUpSrc = "/static/images/PowerUp.png";
var imgPowerUp = new Image();

imgPowerUp.src = imgPowerUpSrc;

// INIT KEYS
let keyStates = {
  ArrowUp: false,
  ArrowDown: false
};
