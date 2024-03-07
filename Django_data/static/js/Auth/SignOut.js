 async function  SignOut() {
  let form = document.getElementById('SignOutForm');
  let formData = new FormData(form);

  const myData = {
    method: 'POST',
    body: formData
  };

  try {
    const response = await fetch(`${ROUTE.SIGNOUT}`, myData);

    if (response.ok) {
      return true;
    }
    else {
      throw new Error('SignOut: A problem occured');
    }
  }
  catch (err) {
    console.error('Error:', err);
  }
  return false;
}
