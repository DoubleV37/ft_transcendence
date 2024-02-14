document.addEventListener('DOMContentLoaded', () => {
  const targetNode = document.querySelector('#content');

  if (!targetNode) {
    console.error('InitMainPage Error: TargetNode not found');
    return;
  }
  
  createObserver(mainCallback);

  const config = { childList: true, subtree: true };

  startObserver(targetNode, config);
});

loadPage(window.location.href);


function mainCallback(mutationsList) {
    for(let mutation of mutationsList) {
        if(mutation.addedNodes.length) {
            const element = document.getElementById('form_signup');
            if (element) {
	      let form = document.getElementById('form_signup');
	      form.addEventListener('submit', async event => {
	      event.preventDefault();
	      signupFormSubmitHandler();
	      });
            }
        }
    }
}
