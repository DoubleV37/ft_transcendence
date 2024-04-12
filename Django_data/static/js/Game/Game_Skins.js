let imgBallSrc = "/static/images/logoIcon.png";
let imgBall = new Image();
imgBall.src = imgBallSrc;

let imgSrcPaddleR = "/static/images/Paddle_Grass.png";
let imgPaddleR = initRotatedImage(imgSrcPaddleR, false); // false pour le paddle droit

let imgSrcPaddleL = "/static/images/Paddle_Grass.png";
let imgPaddleL = initRotatedImage(imgSrcPaddleL, true); // true pour le paddle gauche


function initRotatedImage(imgSrc, isLeftPaddle) {
			let img = new Image();
			let tempCanvas = document.createElement('canvas');
			let initialized = false;
			let rotation = isLeftPaddle ? Math.PI / 2 : -Math.PI / 2; // Calcul de la rotation en fonction du paddle

			img.onload = function() {
				tempCanvas.width = img.height;
				tempCanvas.height = img.width;

				let tempCtx = tempCanvas.getContext('2d');
				tempCtx.translate(tempCanvas.width / 2, tempCanvas.height / 2);
				tempCtx.rotate(rotation); // Rotation selon le sens du paddle
				tempCtx.drawImage(img, -img.width / 2, -img.height / 2);

				initialized = true;
			};

			img.src = imgSrc;

			return {
				canvas: tempCanvas,
				isInitialized: function() {
					return initialized;
				}
			};
		}
