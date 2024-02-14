async function  Tools_RequestBackEnd(myUrl, myData) {
  return fetch(myUrl, myData);
}

function Tools_GetCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");

  if (parts.length === 2){
    return parts.pop().split(";").shift();
  }
}

function addEventListenerById(elementId, eventType, callBackObj) {
  const element = document.getElementById(elementId);
  console.log('aled obj: ' + callBackObj);
  console.log('aled obj nbrparam: ' + callBackObj.nbrParams);
  
  if (element) {
    const myfunc = callBackObj.callBack;

    console.log('function = ' + myfunc);
    switch (callBackObj.nbrParams) {
      case 0:
	element.addEventListener(eventType, myfunc());
	break;
      case 1:
	element.addEventListener( eventType,
				  myfunc(callBackObj.param1));
	break;
      default:
	break;
     }
  }
  else {
    throw new Error(`addEventListenerById: Element with ID ${elementId} not found.`);
  }
}

function CreateEventListeners(param) {
  try {
    for (let Event in param) {
      console.log('Iteration:' + param[Event]);
      addEventListenerById( param[Event].elementId,
			    param[Event].eventType,
			    param[Event].callBackObj);
      //console.log('Element ID = ' + param[Event].elementId);
      //console.log('Event Type = ' + param[Event].eventType);
      //console.log(param[Event].callBack);
    }
  }
  catch (error) {
    console.error(error);
  }
}
