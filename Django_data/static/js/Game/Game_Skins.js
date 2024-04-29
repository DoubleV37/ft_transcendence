let imgBallSrc = "/static/images/logoIcon.png";
let imgBall = new Image();
imgBall.src = imgBallSrc;

let imgSrcPaddleR = "/static/images/Paddle_Grass.png";
let imgPaddleR = initRotatedImage(imgSrcPaddleR, false); // false pour le paddle droit

let imgSrcPaddleL = "/static/images/Paddle_Grass.png";
let imgPaddleL = initRotatedImage(imgSrcPaddleL, true); // true pour le paddle gauche

function initRotatedImage(imgSrc, isLeftPaddle) {
  const img = new Image();
  let initialized = false;
  const tempCanvas = document.createElement("canvas");

  img.onload = function () {
    const rotation = isLeftPaddle ? Math.PI / 2 : -Math.PI / 2;
    const tempCtx = tempCanvas.getContext("2d");

    tempCanvas.width = img.height;
    tempCanvas.height = img.width;

    tempCtx.translate(tempCanvas.width / 2, tempCanvas.height / 2);
    tempCtx.rotate(rotation); // Rotation selon le sens du paddle
    tempCtx.drawImage(img, -img.width / 2, -img.height / 2);

    initialized = true;
  };

  img.src = imgSrc;

  return {
    canvas: tempCanvas,
    isInitialized: function () {
      return initialized;
    }
  };
}

/*function parseUserInfos(infos) {
  try {
    GameInfos.Ball.url = infos.ball;
    GameInfos.Background.url = infos.ball;
    GameInfos.PlayerR.url = infos.paddleR;
    GameInfos.PlayerR.name = infos.nameR;
    GameInfos.PlayerL.url = infos.paddleL;
    GameInfos.PlayerL.name = infos.nameL;
  } catch (err) {
    console.error("Error: ", err);
  }
}

function setGameScreen() {
  GameInfos.Ball.img = new Image();
  GameInfos.Ball.img.src = GameInfos.Ball.url;

  document
    .getElementById("MyCanvas")
    .setAttribute("background-image", `url('${GameInfos.Background.url}')`);

  GameInfos.PlayerR.canvas = initRotatedImage(GameInfos.PlayerR.url, false);
  GameInfos.PlayerL.canvas = initRotatedImage(GameInfos.PlayerL.url, true);
}*/
