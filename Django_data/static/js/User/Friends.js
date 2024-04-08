async function addFriendSubmit() {
  let myForm = document.getElementById('Suggestions');
  let formData = new FormData(myForm);
  formData.append('key', 'add { person }');

  try {
    let response = await MakeRequest(`${ROUTE.FRIENDS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status == 403) {
      return false;
    }
    const data = await response.json();
    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Add Friend ERROR:', err);
    return false;
  }
}

async function deleteFriendSubmit() {

  let myForm = document.getElementById('MyFriends');
  let formData = new FormData(myForm);
  let value = // recuperer la valeur a partir du formulaire
  formData.append('delete', 'add { person }');

  try {
    let response = await MakeRequest(`${ROUTE.FRIENDS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status == 403) {
      return false;
    }
    const data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Delete Friend ERROR:', err);
    return false;
  }
}

