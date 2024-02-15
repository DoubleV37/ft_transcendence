const ROUTE = {
  "HOME":"/",
  "SIGNUP":"/auth/signup",
  "SIGNIN":"/auth/signin"
};

const events_Objects =
  {
    "HOME_PAGE": {
//      "SignOut": {
//	"Id":"SignOut",
//	"eventType": "click",
//	"myFunc": SignOut,
//	"nbrParam": 0
 //     },
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
