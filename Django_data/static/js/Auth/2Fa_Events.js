function  Twofa_SetModalEvents() {
  let element = document.getElementById('2FA_Form');
  element.addEventListener('submit', Twofa_EnableSubmit);
}

function  Twofa_DelModalEvents() {
  let element = document.getElementById('2FA_Form');
  element.removeEventListener('submit', Twofa_EnableSubmit);
}

async function  Twofa_EnableSubmit(event) {
  event.preventDefault();
  let form = document.getElementById('2FA_Form');
  let formData = new FormData(form);
  const	response = await MakeRequest(`${ROUTE.TWOFA_E}`, {
    method: 'POST',
    body: formData
  });
  const data = await response.text();
  console.log(`${data}`);
}
