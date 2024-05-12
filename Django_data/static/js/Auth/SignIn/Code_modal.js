function signin_SetModalEvents () {
  TwofaCodeModal.active = true;
  signin_DelEvents();
  let element = document.getElementById("form_2FAcode");
  element.addEventListener("submit", signin_Code2FACallBack);

  element = document.getElementById("cancel_code2fa");
  element.addEventListener("click", signin_Cancelcode2FACallBack);

  element = document.getElementById("SIGNIN_Form");
  element.addEventListener("submit", signin_PreventSubmit);
}

function signin_DelModalEvents () {
  TwofaCodeModal.active = false;
  let element = document.getElementById("form_2FAcode");
  element.removeEventListener("submit", signin_Code2FACallBack);

  element = document.getElementById("cancel_code2fa");
  element.removeEventListener("click", signin_Cancelcode2FACallBack);

  element = document.getElementById("SIGNIN_Form");
  element.removeEventListener("submit", signin_PreventSubmit);
  signin_SetEvents();
}

function signin_PreventSubmit (event) {
  event.preventDefault();
}

function signin_Cancelcode2FACallBack () {
  TwofaCodeModal.modal.hide();
}

async function	signin_Code2FACallBack (event) {
  event.preventDefault();
  restore_message("success_2FAcode", "failure_2FAcode");

  const	response = await confirm_2FA_SignIn();

  if (response === 403 || response === 404) {
    TwofaCodeModal.modal.hide();
  } else if (response === true) {
    const element = document.getElementById("success_2FAcode");

    element.innerHTML = "2FA authentication succeed.";
    document.getElementById("cancel_code2fa").disabled = true;
    await sleep(1000);
    TwofaCodeModal.modal.hide();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    header_SetEvents();
    loadPage(`${ROUTE.HOME}`);
  } else {
    const element = document.getElementById("failure_2FAcode");

    element.innerHTML = "Wrong code! Please try again.";
  }
}

async function	confirm_2FA_SignIn () {
  const form2FA = document.getElementById("form_2FAcode");
  const formSIGNIN = document.getElementById("SIGNIN_Form");

  const CombinedForm = new FormData();

  for (const pair of new FormData(form2FA)) {
    CombinedForm.append(pair[0], pair[1]);
  }
  for (const pair of new FormData(formSIGNIN)) {
    CombinedForm.append(pair[0], pair[1]);
  }

  const	response = await MakeRequest(`${ROUTE.TWOFA_C}`, {
    method: "POST",
    body: CombinedForm
  });
  if (response.status === 403 || response.status === 404) {
    return 403;
  }
  const data = await response.json();

  return data.success;
}
