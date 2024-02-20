async function  SignOut() {
  const myData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Tools_GetCookie('csrftoken'),
    },
  };

  try {
    let response = await Tools_RequestBackEnd('/auth/signout/', myData);
    let data = await response.json();

    if (data.success == true) {
      showSection('/');
    }
    else {
      alert('Can\'t Sign Out right now');
    }
  }
  catch (err) {
    console.error('Error:', errors);
  }
}
