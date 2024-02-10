async function signupFormSubmitHandler() {
    let form = document.getElementById('form_signup');
    let formData = new FormData(form);

    try {
        const response = await fetch('/auth/signup/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (data["status"] === 'success') {
            console.log("SUCCESS");
            showSection('/');
            history.pushState({section: '/'}, '');
        } else {
            throw new Error('Error submitting form');
        }
    } catch (error) {
	console.error('Error:', error);
        alert('Erreur lors de l’envoi du formulaire');
        showSection('/');
    }
}
