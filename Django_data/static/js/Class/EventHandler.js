//  EventList proto
// {  'Page_ID':'...',
//    'ALL':true/false
//    'DivId':'...', }

class EventHandler {
  constructor(eventData) {
    this.eventData = eventData;
  }

  manageEventListeners(eventList, action) {
    if (action !== 'create' && action !== 'delete') {
      throw new Error(`EventHandler : Wrong action defined -> ${action}`);
    }
    if (eventList['ALL'] && eventList['ALL'] === true) {

    }

  }

  CreateEventListener(target, callBackObj) {
  }

  DeleteEventListener(target, callBackObj) {
  }
}
