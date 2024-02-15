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

function CreateEventListeners(eventObj) {
  try {
    console.log(eventObj);
    for (let element in eventObj) {
      addEventListenerById( eventObj[element].Id,
			    eventObj[element].eventType);
    }
  }
  catch (error) {
    console.error(error);
  }
}

function addEventListenerById(elementId, eventType) {
  const element = document.getElementById(elementId);
  
  if (element) {
    element.addEventListener(eventType, callBackEvent);
  }
  else {
    throw new Error(`addEventListenerById: Element with ID ${elementId} not found.`);
  }
}

function callBackEvent(event) {
  event.preventDefault();

  let element = document.getElementById('titleContent');
  const	titleID = element.getAttribute('data-content');

  element = event.target;
  const	elementID = element.getAttribute('id');
  console.log('titleID = ' + titleID);
  console.log('elementID = ' + elementID);

  const	eventObj = events_Objects[titleID][elementID];

  launchProperCallback(eventObj, event);
}

function  launchProperCallback(eventObj) {
  const	properCallBack = eventObj.myFunc;

  switch (eventObj.nbrParam) {
    case 0:
      properCallBack();
      break ;
    case 1:
      properCallBack(eventObj.param1);
      break ;
    default:
      console.error('Event handler error on : ' + eventObj.Id);
  };
}
