let observer;

//--> Create a New Observer with his associated callback. 
function createObserver(callbackFunction) {
  if (typeof callbackFunction !== 'function') {
    throw new Error('Parameter given isn\'t a function');
  }
  observer = new MutationObserver(callbackFunction);
  return ;
}

//-->Start the Observer.
function startObserver(targetNode, config) {
  observer.observe(targetNode, config);
}

function stopObserver() {
  observer.disconnect();
}
