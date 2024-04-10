async function addFriendSubmit (form) {
  const formData = new FormData(form);
  const button = form.querySelector("button");
  formData.append(`${button.getAttribute("name")}`, `${button.getAttribute("value")}`);

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData
    });

    if (response.status === 403) {
      return false;
    }
    const data = await response.json();
    if (data.success === true) {
      return true;
    } else {
      myForm.reset();
      return false;
    }
  } catch (err) {
    console.error("Add Friend ERROR:", err);
    return false;
  }
}

async function deleteFriendSubmit () {
  const myForm = document.getElementById("MyFriends");
  const formData = new FormData(myForm);
  const value = // recuperer la valeur a partir du formulaire
  formData.append("delete", "add { person }");

  try {
    const response = await MakeRequest(`${ROUTE.FRIENDS}`, {
      method: "POST",
      body: formData
    });

    if (response.status === 403) {
      return false;
    }
    const data = await response.json();

    if (data.success === true) {
      return true;
    } else {
      myForm.reset();
      return false;
    }
  } catch (err) {
    console.error("Delete Friend ERROR:", err);
    return false;
  }
}
