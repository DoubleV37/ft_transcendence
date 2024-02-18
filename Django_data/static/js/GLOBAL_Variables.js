let currentUrl = window.location.pathname;
let observer;

const ROUTE = {
  "HOME":"/",
  "SIGNUP":"/auth/signup",
  "SIGNIN":"/auth/signin"
};

const EventList =
  {
    "HOME_PAGE": {
      "SignIn": {
	"Id":"SignIn",
	"eventType": "click",
	"myFunc": loadPage,
	"nbrParam": 1,
	"param1": `${ROUTE.SIGNIN}`
      }
    },
    "SIGN_IN": {
      "signinForm": {
	"Id": "signinForm",
	"eventType": "submit",
	"myFunc": SignIn,
	"nbrParam": 0
	},
      "signup": {
	"Id": "signup",
	"eventType": "click",
	"myFunc": loadPage,
	"nbrParam": 1,
	"param1": `${ROUTE.SIGNUP}`
      }
    }
  }
