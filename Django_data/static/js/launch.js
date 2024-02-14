document.addEventListener('DOMContentLoaded', () => {
  const targetNode = document.querySelector('#content');

  if (!targetNode) {
    console.error('InitMainPage Error: TargetNode not found');
    return;
  }
  
  createObserver(callBack);

  const config = { childList: true, subtree: true };

  startObserver(targetNode, config);
});

let currentUrl = window.location.pathname;

loadPage(currentUrl);
