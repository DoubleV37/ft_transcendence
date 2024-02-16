//----------Run at the load/reload of the website-------------//
document.addEventListener('DOMContentLoaded', launchWebsite);
console.log(eventHandler);

function  launchWebsite() {
  const targetNode = document.querySelector('#content');

  if (!targetNode) {
    console.error('InitMainPage Error: TargetNode not found');
    return;
  }

  const config = { childList: true, subtree: true };

  observer = new MutationObserver(callbackFunction);
  startObserver(targetNode, config);

  loadPage(currentUrl);
  triggerFirstEvent();

  document.removeEventListener('DOMContentLoaded', launchWebsite);
}

function  triggerFirstEvent() {
  const	element = document.getElementById('titleContent');

  if (!element) {
    console.log('Fuck it...');
    return ;
  }
  const	ID = element.getAttribute('data-content');
  //CreateEventListeners(ID);
}
//-----------------------------------------------------------//

function callBack(mutationsList) {
  for(let mutation of mutationsList) {
    if(mutation.type === 'childList') {
      const element = document.getElementById('titleContent');

      if (!element) {
	continue ;
      }
//      CreateEventListeners(events_Objects[element.dataset.content]);
    }
  }
}
