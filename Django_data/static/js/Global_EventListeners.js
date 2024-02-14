const ROUTE = {
  "HOME":"/",
  "SIGNUP":"/auth/signup",
  "SIGNIN":"/auth/signin"
};

const signin_Object =
  {
    "event1": {
      "elementId": "signinForm",
      "eventType": "submit",
      "callBackObj": {
	"nbrParams": 0,
	"callBack":SignIn
      }
    },
    "event2": {
      "elementId": "signup",
      "eventType": "click",
      "callBackObj": {
	"nbrParams": 1,
	"callBack": loadPage,
	"param1": `${ROUTE.HOME}`
      }
    }
  };
