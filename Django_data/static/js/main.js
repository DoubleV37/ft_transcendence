//----------Run at the load/reload of the website-------------//
document.addEventListener('DOMContentLoaded', launchWebsite);


async function  launchWebsite() {
  const targetNode = document.querySelector('#content');

  if (!targetNode) {
    console.error('InitMainPage Error: TargetNode not found');
    return;
  }

  const config = { childList: true, subtree: true };

  observer = new MutationObserver(mutationCallBack);
  observer.observe(targetNode, config);

  await loadPage(currentUrl);
  await changeSection(`${ROUTE.HEADER}`, '#Header_content');
  modal_ProfileInit();
  header_SetEvents();
  main_SetFirstsEvents();

  document.removeEventListener('DOMContentLoaded', launchWebsite);
 }

function  main_SetFirstsEvents() {
   const	element = document.getElementById('titleContent');

   if (!element) {
     console.log('Fuck it...');
     return ;
   }
   launchSectionHandler(element);
}
//-----------------------------------------------------------//

function mutationCallBack(mutationsList) {
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

function  launchSectionHandler(element) {
  const elementAttribut = element.getAttribute('data-content');

  try {
    switch(elementAttribut) {
      case 'HOME_PAGE':
	home_SetEvents();
	break ;
      case 'SIGNIN_PAGE':
        signin_SetEvents();
        break ;
      case 'SIGNUP_PAGE':
        signup_SetEvents();
        break ;
      case 'SETTINGS':
        settings_SetEvents();
        modal_AvatarInit();
        header_SetEvents();
	break ;

      default:
	throw new Error(`launchSectionHandler: Attribute ${elementAttribut} non recognised`);
    }
  }
  catch (err) {
    console.error('Error: ', err);
  }
}
