//function callBack(mutationsList) {
//  for(let mutation of mutationsList) {
//    if(mutation.addedNodes.length) {
//      const element = document.getElementById('form_signup');
//      if (element) {
//	let form = document.getElementById('form_signup');
//	form.addEventListener('submit', async event => {
//	  event.preventDefault();
//	  signupFormSubmitHandler();
//	});
//      }
//    }
//  }
//}

function callBack(mutationsList) {
  for(let mutation of mutationsList) {
    if(mutation.type === 'childList') {
      const element = document.getElementById('titleContent');

      if (!element) {
	continue ;
      }
      caseSelector(element.dataset.content);
    }
  }
}
