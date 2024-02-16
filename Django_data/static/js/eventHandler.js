function HandleEventListeners(eventObj, flag) {
  try {
    if (!eventObj) {
      throw new Error('CreateEventListeners : function parameters error'); //DEBUG
    }
    let	eventFunction;

    switch (flag) {
      case 'create':
	eventFunction = addEventListenerById;
	break ;
      case 'erase':
	eventFunction = eraseEventListenerById;
	break ;
      default:
	throw new Error(`HandleEventListeners : Wrong flag ${flag}`);
    }
    for (let element in eventObj) {
      eventFunction(eventObj[element].Id,
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
    throw new Error(`addEventListenerById: Element with ID ${elementId} not found.`); //DEBUG
  }
}

function callBackEvent(event) {
  event.preventDefault();

  let element = document.getElementById('titleContent');
  const	titleID = element.getAttribute('data-content');

  element = event.target;
  const	elementID = element.getAttribute('id');
  console.log('titleID = ' + titleID); //DEBUG
  console.log('elementID = ' + elementID); //DEBUG

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
      console.error('Event handler error on : ' + eventObj.Id); //DEBUG
  };
}
