console.log('signup.js');
let form = document.getElementById('signup_form');
form.addEventListener('submit', async event => {
	event.preventDefault();
	let formData = new FormData(form);
	try {
		const response = await fetch('/auth/signup/', {
			method: 'POST',
			body: formData
		});
		const data = await response.json();

		if (data["status"] === 'success') {
			console.log("SUCCESS");
			// Uncomment the following lines if you want to redirect after successful submission
			showSection('/');
			// history.pushState({section: '/'}, '');
		} else {
			throw new Error('Error submitting form');
		}
	} catch (error) {
		alert('Erreur lors de l’envoi du formulaire');
		showSection('/');
	}
});
