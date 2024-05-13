function signin_SetEvents () {
  let element = document.getElementById("SIGNIN_Form");
  element.addEventListener("submit", signin_FormCallBack);

  element = document.querySelector("#SIGNIN_Signup b");
  element.addEventListener("click", signin_SignUpCallBack);
}

function signin_DelEvents () {
  let element = document.getElementById("SIGNIN_Form");
  element.removeEventListener("submit", signin_FormCallBack);

  element = document.querySelector("#SIGNIN_Signup b");
  element.removeEventListener("click", signin_SignUpCallBack);
}

async function signin_FormCallBack (event) {
  event.preventDefault();
  const	response = await signIn();

  if (response == true) {
    signin_DelEvents();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    await loadPage(`${ROUTE.HOME}`);
    header_SetEvents();
  }
}

async function signin_SignUpCallBack () {
  signin_DelEvents();
  await loadPage(`${ROUTE.SIGNUP}`);
}
