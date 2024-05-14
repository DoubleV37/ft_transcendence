async function nameSubmit() {
  const myForm = document.getElementById('NAME_Form');
  const formData = new FormData(myForm);
  formData.append('name_button', 'name_button');

  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    const data = await response.json();

    if (data.success === true) {
      return true;
    }
	  myForm.reset();
	  return false;
  } catch (err) {
    console.error('Name Errors:', err);
    return false;
  }
}

async function mailSubmit() {
  const myForm = document.getElementById('MAIL_Form');
  const formData = new FormData(myForm);
  formData.append('mail_button', 'mail_button');

  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    const data = await response.json();

    if (data.success === true) {
      return true;
    }
    myForm.reset();
	  return false;
  } catch (err) {
    console.error('Mail Errors:', err);
    return false;
  }
}

async function passSubmit() {
  const myForm = document.getElementById('PASS_Form');
  const formData = new FormData(myForm);
  formData.append('pswd_button', 'pswd_button');

  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    const data = await response.json();

    if (data.success === true) {
      return true;
    }
    myForm.reset();
	  return false;
  } catch (err) {
    console.error('Pass Errors:', err);
    return false;
  }
}

async function tnameSubmit() {
  const myForm = document.getElementById('TNAME_Form');
  const formData = new FormData(myForm);
  formData.append('t_name_button', 't_name_button');

  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    const data = await response.json();

    if (data.success === true) {
      return true;
    }
	  myForm.reset();
	  return false;
  } catch (err) {
    console.error('TName Errors:', err);
    return false;
  }
}

async function avatarSubmit() {
  const myForm = document.getElementById('AVATAR_Form');
  const formData = new FormData(myForm);
  formData.append('avatar_button', 'avatar_button');
  
  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return response.status;
    }
    const data = await response.json();
    
    if (data.success === true) {
      return true;
    }
	  myForm.reset();
    document.getElementById("ErrorAvatar").innerHTML = 'Error on submit!';
	  return false;
  } catch (err) {
    console.error('Avatar Errors:', err);
    return false;
  }
}

async function del_avatarSubmit() {
  const myForm = document.getElementById('DEL_AVATAR_Form');
  const formData = new FormData(myForm);
  formData.append('avatar_delete', 'avatar_delete');
  
  try {
    const response = await MakeRequest(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });

    if (response.status === 403 || response.status === 404) {
      return false;
    }
    const data = await response.json();
    
    if (data.success === true) {
      return true;
    }
	  myForm.reset();
	  return false;
  } catch (err) {
    console.error('Avatar Delete Errors:', err);
    return false;
  }
}