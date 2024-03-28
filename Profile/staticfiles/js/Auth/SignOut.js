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
    const data = await response.json();

    if (data.success == true) {
      changeSection(`${ROUTE.HOME}`, '#content');
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
