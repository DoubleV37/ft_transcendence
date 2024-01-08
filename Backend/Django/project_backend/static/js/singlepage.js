function showSection(section) {
	fetch(`${section}`)
	.then(response => response.text())
	.then(text => {
		document.querySelector('#content').innerHTML = text;
	});

}


document.addEventListener("DOMContentLoaded", function() {
	if (page == 'index') {
		document.querySelectorAll('button').forEach(button => {
			button.onclick = function() {
				showSection(this.dataset.section)
				history.pushState({section: this.dataset.section}, '', this.dataset.section)
				window.onpopstate = function(event) {
					showSection(event.state.section)
				}
			}
		})
	}
	else {
		fetch(`${header}`)
		.then(response => response.text())
		.then(text => {
			document.querySelector('#header').innerHTML = text;
		});
		fetch(`${footer}`)
		.then(response => response.text())
		.then(text => {
			document.querySelector('#footer').innerHTML = text;
		});

	}
});
