function skins_SetEvents () {
  const element = document.getElementById("Save_Skins");

  element.addEventListener("click", skins_SaveAll);
}

function skins_DelEvents () {
  const element = document.getElementById("Save_Skins");

  element.removeEventListener("click", skins_SaveAll);
}

async function skins_SaveAll (event) {
  const paddleItem = document
    .getElementById("paddleInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  const ballItem = document
    .getElementById("ballInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");
  const backgroundItem = document
    .getElementById("backgroundInner")
    .querySelector(".carousel-item.active")
    .getAttribute("data-skin");

  try {
    const response = await MakeRequest(`${ROUTE.SKINS}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": event.target.querySelector("input").getAttribute("value")
      },
      mode: "same-origin",
      body: JSON.stringify({
        paddle: paddleItem,
        ball: ballItem,
        background: backgroundItem
      })
    });
    if (response.status === 403) {
      return ;
    }
    const data = await response.json();

    if (data.success === true) {
      document.getElementById("SkinsMessage").setAttribute("style", "color: green;");
      document.getElementById("SkinsMessage").innerHTML = "Skins successfully changed!";
    } else {
      document.getElementById("SkinsMessage").setAttribute("style", "color: red;");
      document.getElementById("SkinsMessage").innerHTML = "Something went wrong!";
    }
  } catch (err) {
    console.error("Skins Errors:", err);
  }
}
