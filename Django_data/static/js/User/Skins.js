lol
function skins_SetEvents() {
  const element = document.getElementById("Save_Skins");

  element.addEventListener("click", skins_SaveAll);
}

function skins_DelEvents() {
  const element = document.getElementById("Save_Skins");

  element.removeEventListener("click", skins_SaveAll);
}

function skins_SaveAll() {
  console.log("HELLO from skins_SaveAll");
}
