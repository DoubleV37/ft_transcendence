async function nameSubmit() {

  let myForm = document.getElementById('NAME_Form');
  let formData = new FormData(myForm);
  formData.append('name_button', 'name_button');

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });
    const data = await response.json();
    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Name Errors:', err);
    return false;
  }
}

async function mailSubmit() {

  let myForm = document.getElementById('MAIL_Form');
  let formData = new FormData(myForm);
  formData.append('mail_button', 'mail_button');

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });
    const data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Mail Errors:', err);
    return false;
  }
}

async function passSubmit() {

  let myForm = document.getElementById('PASS_Form');
  let formData = new FormData(myForm);
  formData.append('pswd_button', 'pswd_button');

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });
    const data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Pass Errors:', err);
    return false;
  }
}

async function tnameSubmit() {

  let myForm = document.getElementById('TNAME_Form');
  let formData = new FormData(myForm);
  formData.append('t_name_button', 't_name_button');

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
    method: 'POST',
	  body: formData
    });
    const data = await response.json();

    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('TName Errors:', err);
    return false;
  }
}

async function avatarSubmit() {
  let myForm = document.getElementById('AVATAR_Form');
  let formData = new FormData(myForm);
  formData.append('avatar_button', 'avatar_button');
  
  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    
    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Avatar Errors:', err);
    return false;
  }
}

async function del_avatarSubmit() {
  let myForm = document.getElementById('DEL_AVATAR_Form');
  let formData = new FormData(myForm);
  formData.append('avatar_delete', 'avatar_delete');
  

  try {
    let response = await fetch(`${ROUTE.SETTINGS}`, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    
    if (data.success == true) {
      return true;
    }
    else {
	myForm.reset();
	return false;
    }
  }
  catch (err) {
    console.error('Avatar Delete Errors:', err);
    return false;
  }
}
