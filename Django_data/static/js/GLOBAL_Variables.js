let currentUrl = window.location.pathname;
let observer;
let _2faSignIn = false;

let error403 = false;

let profileModal = {
  modal: null,
  active: false,
};

let avatarModal = {
  modal: null,
  active: false,
};

let TwofaModal = {
  modal: null,
  active: false,
};

let TwofaCodeModal = {
  modal: null,
  active: false,
};

let friendsModal = {
  modal: null,
  active: false,
};

let GameParams = {
  Opponent: "ai",
  Type: "local",
  Score: 3,
  Difficulty: 5,
  PowerUp: false,
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
  FRIENDS: "/friends/list/",
  REQUESTS: "/friends/request/",
  TWOFA_E: "/2fa/enable/",
  TWOFA_Q: "/2fa/qrcode/",
  TWOFA_C: "/2fa/confirm/",
  JWTREFRESH: "/auth/jwt/refresh/",
  GAME_PARAMETERS: "/game/parameters/",
  GAME_MODES: "/game/modes/",
};
