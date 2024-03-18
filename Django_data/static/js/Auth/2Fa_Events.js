function  Twofa_SetModalEvents() {
  let element = document.getElementById('form_2FA');
  element.addEventListener('submit', Twofa_EnableSubmit);

  element = document.getElementById('cancel_2fa');
  element.addEventListener('click', Twofa_CancelSubmit);
}

function  Twofa_DelModalEvents() {
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
    Twofa_DelModalEvents();
    TwofaModal.hide();
    settings_DelEvents();
    changeSection(`${ROUTE.SETTINGS}`, `#content`);
}

async function  Twofa_EnableSubmit(event) {
  event.preventDefault();
  restore_message();
  const form = document.getElementById('form_2FA');
  const formData = new FormData(form);
  const	response = await MakeRequest(`${ROUTE.TWOFA_C}`, {
    method: 'POST',
    body: formData
  });
  const data = await response.json();
  console.log(`conf response => ${data.success}`);
  if (data.success == true) {
    let element = document.getElementById('success_2FA');

    element.innerHTML = `2FA authentication successfully enabled.`;
    _2faOngoing = false;
    Twofa_DelModalEvents();
    await sleep(2000);
    TwofaModal.hide();
  }
  else {
    let element = document.getElementById('failure_2FA');

    element.innerHTML = `Error: Wrong code submitted. Please try again.`;
  }
}

function  restore_message() {
  let element = document.getElementById('failure_2FA');

  element.innerHTML = ``;
  element = document.getElementById('success_2FA');

  element.innerHTML = ``;
}
