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
  message: "settings",
  opponent: "ai",
  type: "local",
  point_limit: 3,
  difficulty: 5,
  powerup: false,
};

let iaMemory = {
  pos: 450,
  target: 450,
  step: 20,
  service : false
};

const ROUTE = {
  HOME: "/",
  HEADER: "/header",
  FOOTER: "/footer",
  PING: "/auth/ping/",
  SIGNUP: "/auth/signup/",
  SIGNIN: "/auth/signin/",
  SIGNOUT: "/auth/signout/",
  SETTINGS: "/auth/settings/",
  PROFILE: "/user/profile/",
  SKINS: "/user/skins/",
  FRIENDS_PROFILE: "/friends/profile/",
  FRIENDS: "/friends/list/",
  REQUESTS: "/friends/request/",
  TWOFA_E: "/2fa/enable/",
  TWOFA_Q: "/2fa/qrcode/",
  TWOFA_C: "/2fa/confirm/",
  JWTREFRESH: "/auth/jwt/refresh/",
  GAME_PARAMETERS: "/game/parameters/",
  GAME_MODES: "/game/modes/",
  GAME_MATCH: "/game/matchmaking/",
  GAME_ROOM:"/game/", //`${ROUTE.GAME_ROOM}${id...}/`
  GAME_LOCAL: "/game/solo/",
};

// INIT POWERUP
let imgPowerUpSrc = "/static/images/PowerUp.png";
let imgPowerUp = new Image();

imgPowerUp.src = imgPowerUpSrc;

// INIT KEYS
let keyStates = {
  ArrowUp: false,
  ArrowDown: false,
  w: false,
  s: false,
  space: false
};

// INIT CANVAS
let gameCanvas = {
  canvas: null,
  ctx: null,
  style: null,
  width: 0,
  height: 0,
  paddle1Height: 0,
  paddle2Height: 0,
  powerup: false,
  powerupY: 0,
  powerupX: 0,
  powerupsize: 0,
  ballRadius: 0,
  opponent: "",
  num: 0,
  inGame: true
};

//MATCHMAKING SCREEN
let dots = 0;
let idDot;

let gameSocket = null;
let gameStop = true;
