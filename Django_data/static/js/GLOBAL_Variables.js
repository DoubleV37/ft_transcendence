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

/*-----------Routes-----------*/
const ROUTE = {
  HOME: "/",
  HEADER: "/header",
  FOOTER: "/footer",
  ERROR404: "/404",
  PING: "/auth/ping/",
  SIGNUP: "/auth/signup/",
  SIGNIN: "/auth/signin/",
  SIGNOUT: "/auth/signout/",
  SETTINGS: "/auth/settings/",
  PROFILE: "/user/profile/",
  GAMELIST: "/dash/history/",
  GAMEBOARD: "/dash/board/",
  STATS: "/dash/stats/",
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
  GAME_ROOM: "/game/",
  GAME_LOCAL: "/game/solo/",
  SET_TOURNAMENT: "/game/tournament/set/",
  BRACKET_TOURNAMENT: "/game/tournament/bracket/"
};

/*-----------Game Parameters-----------*/
let GameParams = {
  message: "settings",
  opponent: "ai",
  type: "local",
  point_limit: 3,
  difficulty: 5,
  powerup: false,
  type_game: "all"
};

let GameInfos = {
  num: 0,
  Ball: {
    url: "", // img url
    img: null // img obj
  },
  Background: {
    url: ""
  },
  PlayerR: {
    srcImg: "", // img url
    srcPaddle: "", // img url
    canvas: null, // img obj
    name: ""
  },
  PlayerL: {
    srcImg: "",
    srcPaddle: "",// img url
    canvas: null, // img obj
    name: ""
  }
};


let iaMemory = {
  pos: 450,
  target: 450,
  step: 20,
  service: false
};

/*----------Key State of game-----------*/
let keyStates = {
  ArrowUp: false,
  ArrowDown: false,
  w: false,
  s: false,
  space: false
};

/*----------Canvas variables-----------*/
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

let multi = false;
let lastFrameTime = 0;
const targetFrameRate = 90;

let imgPowerUpSrc = "/static/images/PowerUp.png";
let imgPowerUp = new Image();

imgPowerUp.src = imgPowerUpSrc;

let loading = false;
let deleteEvent = false;

/*-----------Socket and status Game-----------*/
let gameSocket = null;
let matchSocket = null;
let gameStop = true;

let tournament = null;
let playerVictorySrc = "/static/images/penguin-dance.gif";
let defeatSrc = "/static/images/shiny-charmander-pokemon.gif";
let stoppedSrc = "/static/images/ghost-phantom.gif";
let aiVictorySrc = "/static/images/darth-vader.gif";
