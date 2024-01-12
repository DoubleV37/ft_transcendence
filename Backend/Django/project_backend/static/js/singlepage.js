function showSection(section) {
	fetch(`${section}`)
	.then(response => response.text())
	.then(text => {
		var tempDiv = document.createElement('div');
		tempDiv.innerHTML = text;

		// Récupérer le contenu de la balise avec l'ID 'content' de la page fetchée
		var fetchedContent = tempDiv.querySelector('#content'); //ya pb la

		// Insérer le contenu dans la balise avec l'ID 'content' de la page actuelle
		var currentContentElement = document.querySelector('#content');
		currentContentElement.innerHTML = fetchedContent.innerHTML;
		// document.querySelector('#content').innerHTML = text;
	});
}

document.addEventListener("DOMContentLoaded", function() {
	if (page != 'index') {
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
		page = 'index'
	}

	document.querySelectorAll('button').forEach(button => {
		button.onclick = function() {
			showSection(this.dataset.section)
			history.pushState({section: this.dataset.section}, '', this.dataset.section)
			window.onpopstate = function(event) {
				showSection(event.state.section)
			}
		}
	})
});

function clickButton(button) {
	showSection(button.dataset.section)
	history.pushState({section: button.dataset.section}, '', button.dataset.section)
	window.onpopstate = function(event) {
		showSection(event.state.section)
	}
}
