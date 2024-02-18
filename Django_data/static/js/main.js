//----------Run at the load/reload of the website-------------//
document.addEventListener('DOMContentLoaded', launchWebsite);


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
  launchSectionHandler(element);
}
//-----------------------------------------------------------//

function callBack(mutationsList) {
  for(let mutation of mutationsList) {
    if(mutation.type === 'childList') {
      const element = document.getElementById('titleContent');

      if (!element) {
	      continue ;
      }
      
      launchSectionHandler(element);
    }
  }
}

launchSectionHandler(element) {
  const elementAttribut = element.getAttribute('data-content');

  switch(elementAttribut) {
    case 'HOME_PAGE':
      setHomePage();
      break ;
    case 'SIGNIN_PAGE':
      setSingIn_PAGE();
      break ;
//    .
//    .
//    .
    default:
      throw new Error(`launchSectionHandler: Attribute ${elementAttribut} non recognised`);
  }
}
