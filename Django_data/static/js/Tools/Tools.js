async function  Tools_RequestBackEnd(myUrl, myData) {
  return fetch(myUrl, myData)
    .then(response => response.json())
    .catch(error => {
      console.error('Error:', error);
    });
}

function Tools_GetCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");

    if (parts.length === 2){
      return parts.pop().split(";").shift();
    }
}
