let currentUrl = window.location.pathname;

document.addEventListener('DOMContentLoaded', launchWebsite);

function  launchWebsite() {
  const targetNode = document.querySelector('#content');

  if (!targetNode) {
    console.error('InitMainPage Error: TargetNode not found');
    return;
  }

  createObserver(callBack);

  const config = { childList: true, subtree: true };

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
  caseSelector(ID);
}
