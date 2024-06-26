function Twofa_SetModalEvents () {
  let element = document.getElementById("form_2FA");
  element.addEventListener("submit", Twofa_EnableSubmit);

  element = document.getElementById("cancel_2fa");
  element.addEventListener("click", Twofa_CancelSubmit);
}

function Twofa_DelModalEvents () {
  let element = document.getElementById("form_2FA");
  element.removeEventListener("submit", Twofa_EnableSubmit);

  element = document.getElementById("cancel_2fa");
  element.removeEventListener("click", Twofa_CancelSubmit);
}

async function	Twofa_CancelSubmit () {
  const form = document.getElementById("form_2FA");
  const formData = new FormData(form);
  await MakeRequest(`${ROUTE.TWOFA_E}`, {
    method: "POST",
    body: formData
  });
  Twofa_DelModalEvents();
  TwofaModal.hide();
  settings_DelEvents();
  try {
    changeSection(`${ROUTE.SETTINGS}`, "#content");
  } catch (err) {
    console.error("Error:", err);
  }
}

async function Twofa_EnableSubmit (event) {
  event.preventDefault();
  restore_message("success_2FA", "failure_2FA");
  const form = document.getElementById("form_2FA");
  const formData = new FormData(form);
  const	response = await MakeRequest(`${ROUTE.TWOFA_C}`, {
    method: "POST",
    body: formData
  });
  const data = await response.json();
  if (data.success == true) {
    const element = document.getElementById("success_2FA");

    element.innerHTML = "2FA authentication successfully enabled.";
    Twofa_DelModalEvents();
    await sleep(2000);
    TwofaModal.hide();
  } else {
    const element = document.getElementById("failure_2FA");

    element.innerHTML = "Error: Wrong code submitted. Please try again.";
  }
}

function Error_Page (code) {
  try {
    if (code === 403) {
      loadPage(currentUrl);
    } else {
      errorCode = true;
      loadPage(ROUTE.ERROR404);
    }
  } catch (err) {
    console.error("Error:", err);
  }
}
