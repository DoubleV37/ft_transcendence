function showSection(section) {
	fetch(`${section}`)
	.then(response => response.text())
	.then(text => {
		let tempDiv = document.createElement('div');
		tempDiv.innerHTML = text;

		// Récupérer le contenu de la balise avec l'ID 'content' de la page fetchée
		let fetchedContent = tempDiv.querySelector('#content');

		// Remplacer le contenu de la balise avec l'ID 'content' de la page actuelle par le contenu de la balise avec l'ID 'content' de la page fetchée
		document.querySelector('#content').innerHTML = fetchedContent.innerHTML;
	});
}

function clickButton(button) {
	showSection(button.dataset.section)
	history.pushState({section: button.dataset.section}, '')
}

window.onpopstate = function(event) {
	if (event.state == null) {
		showSection('')
		return
	}
	showSection(event.state.section)
}

function callback(mutationsList) {
    for(let mutation of mutationsList) {
        if(mutation.addedNodes.length) {
            const element = document.getElementById('form_signup');
            if (element) {
				let form = document.getElementById('form_signup');
				form.addEventListener('submit', async event => {
					event.preventDefault();
					signupFormSubmitHandler()
				});
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
	const targetNode = document.querySelector('#content');
	if (!targetNode) {
        console.error('Target node not found');
        return;
    }
	// Create an instance of MutationObserver with the defined callback
	const observer = new MutationObserver(callback);

	// Specify the configuration to observe
	const config = { childList: true, subtree: true };

	// Start observing the target node for configured mutations
	observer.observe(targetNode, config);
});
