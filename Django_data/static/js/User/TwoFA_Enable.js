function  Twofa_SetModalEvents() {
  TwofaModal['active'] = true;
  let element = document.getElementById('form_2FA');
  element.addEventListener('submit', Twofa_EnableSubmit);

  element = document.getElementById('cancel_2fa');
  element.addEventListener('click', Twofa_CancelSubmit);
}

function  Twofa_DelModalEvents() {
  TwofaModal['active'] = false;
  let element = document.getElementById('form_2FA');
  element.removeEventListener('submit', Twofa_EnableSubmit);

  element = document.getElementById('cancel_2fa');
  element.removeEventListener('click', Twofa_CancelSubmit);
}

async function	Twofa_CancelSubmit() {
  let form = document.getElementById('form_2FA');
  let formData = new FormData(form);

  await MakeRequest(`${ROUTE.TWOFA_E}`, {
    method: 'POST',
    body: formData
  });
  TwofaModal['modal'].hide();
  settings_DelEvents();
  try {
    changeSection(`${ROUTE.SETTINGS}`, `#content`);
  } catch (err) {
    console.error("Error:", err);
  }
}

async function  Twofa_EnableSubmit(event) {
  event.preventDefault();
  restore_message('success_2FA', 'failure_2FA');

  const form = document.getElementById('form_2FA');
  const formData = new FormData(form);
  try {
    const	response = await MakeRequest(`${ROUTE.TWOFA_C}`, {
      method: 'POST',
      body: formData
    });
    if (response.status === 403) {
      TwofaModal.modal.hide();
      return ;
    }
    const data = await response.json();

    if (data.success === true) {
      let element = document.getElementById('success_2FA');

      element.innerHTML = `2FA authentication successfully enabled.`;
      document.getElementById("TwofaModal").querySelector("#cancel_2fa").disabled = true;
      await sleep(1000);
      TwofaModal['modal'].hide();
    } else {
      let element = document.getElementById('failure_2FA');

      element.innerHTML = `Error: Wrong code submitted. Please try again.`;
    }
  } catch (err) {
    console.error("2FA Error: ", err);
  }
}
