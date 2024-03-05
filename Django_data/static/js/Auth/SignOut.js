async function  SignOut() {
  const myData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Tools_GetCookie('csrftoken'),
    },
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
