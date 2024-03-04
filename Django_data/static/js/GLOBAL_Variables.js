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
  // "SETTINGS":"/user/settings/",
  "SETTINGS":"/auth/settings/",
  "PROFILE":"/user/profile/",
};
