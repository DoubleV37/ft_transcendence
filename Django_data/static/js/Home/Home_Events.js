function  home_SetEvents() {
  let element = document.getElementById('PlayButton');

  element.addEventListener('click', PlayCallBack);
}

function  home_DelEvents() {
  let element = document.getElementById('PlayButton');

  element.removeEventListener('click', PlayCallBack);
}

function  PlayCallBack() {
    console.log("Do nothing for now");
}
