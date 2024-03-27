async function Access_Denied(response) {
  let newHTML = document.open("text/html", "replace");
  newHTML.write(response);
  newHTML.close();
}
