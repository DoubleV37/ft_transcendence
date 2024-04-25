function skins_SetEvents () {
  const element = document.getElementById("Save_Skins");

  element.addEventListener("click", skins_SaveAll);
}

function skins_DelEvents () {
  const element = document.getElementById("Save_Skins");

  element.removeEventListener("click", skins_SaveAll);
}

async function skins_SaveAll () {
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
      method: 'POST',
      body: JSON.stringify({
        paddle: paddleItem,
        ball: ballItem,
        background: backgroundItem
      })
    });
    if (!response.ok)
}
