function  SignOut() {
  let myData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Tools_GetCookie('csrftoken'),
    },
  };

  Tools_RequestBackEnd('/auth/signout/', myData);
  clickButton(document.getElementById('SignOut'));
}
