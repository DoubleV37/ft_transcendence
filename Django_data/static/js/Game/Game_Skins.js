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

function parseUserInfos(infos) {
  GameInfos.Ball.url = infos.my_ball;
  GameInfos.Background.url = infos.my_background;
  if (infos.num === 1) {
    GameInfos.PlayerR.srcImg = `/static/${infos.my_avatar}`;
    GameInfos.PlayerR.srcPaddle = `/static/${infos.my_paddle}`;
    GameInfos.PlayerR.name = infos.my_name;
    GameInfos.PlayerL.srcImg = infos.opponent_avatar;
    GameInfos.PlayerL.srcPaddle = infos.opponent_paddle;
    GameInfos.PlayerL.name = infos.opponent_name;
  } else {
    GameInfos.PlayerR.srcImg = infos.opponent_avatar;
    GameInfos.PlayerR.srcPaddle = infos.opponent_paddle;
    GameInfos.PlayerR.name = infos.opponent_name;
    GameInfos.PlayerL.srcImg = infos.my_avatar;
    GameInfos.PlayerL.srcPaddle = infos.my_paddle;
    GameInfos.PlayerL.name = infos.my_name;
  }
}

function setGameScreen() {
  GameInfos.Ball.img = new Image();
  GameInfos.Ball.img.src = GameInfos.Ball.url;

  GameInfos.PlayerR.canvas = initRotatedImage(GameInfos.PlayerR.url, false);
  GameInfos.PlayerL.canvas = initRotatedImage(GameInfos.PlayerL.url, true);
}
