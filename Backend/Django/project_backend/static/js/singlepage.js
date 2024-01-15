function showSection(section) {
	fetch(`${section}`)
	.then(response => response.text())
	.then(text => {
		var tempDiv = document.createElement('div');
		tempDiv.innerHTML = text;

		// Récupérer le contenu de la balise avec l'ID 'content' de la page fetchée
		var fetchedContent = tempDiv.querySelector('#content');

		// Remplacer le contenu de la balise avec l'ID 'content' de la page actuelle par le contenu de la balise avec l'ID 'content' de la page fetchée
		document.querySelector('#content').innerHTML = fetchedContent.innerHTML;
	});
}

document.addEventListener("DOMContentLoaded", function() {
	fetch('header')
	.then(response => response.text())
	.then(text => {
		document.querySelector('#header').innerHTML = text;
	});
	fetch('footer')
	.then(response => response.text())
	.then(text => {
		document.querySelector('#footer').innerHTML = text;
	});
});

function clickButton(button) {
	showSection(button.dataset.section)
	history.pushState({section: button.dataset.section}, '', button.dataset.section)
}

window.onpopstate = function(event) {
	if (event.state == null) {
		showSection('')
		return
	}
	showSection(event.state.section)
}
