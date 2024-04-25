function drawPaddleR(y) {
    if (imgPaddleR.isInitialized()) {
        // Calculer les coordonnées exactes pour le dessin du paddle droit
        let x = gameCanvas.canvas.width - (gameCanvas.canvas.width * 50 / 1200) - (gameCanvas.canvas.height * 25 / 900) + (gameCanvas.canvas.height * 25 / 900); // Prend en compte la largeur du paddle
        let height = gameCanvas.paddle2Height;
        let width = gameCanvas.canvas.height * 25 / 900;
        let deltaY = y * gameCanvas.canvas.height - height / 2;

        // Ajuster les coordonnées pour éviter les imprécisions
        x = Math.floor(x);
        deltaY = Math.floor(deltaY);
        width = Math.round(width);
        height = Math.round(height);

        gameCanvas.ctx.drawImage(imgPaddleR.canvas, x, deltaY, width, height);
    }
}

function drawPaddleL(y) {
    if (imgPaddleL.isInitialized()) {
        // Calculer les coordonnées exactes pour le dessin du paddle gauche
        let x = (gameCanvas.canvas.width * 50 / 1200) - (gameCanvas.canvas.height * 25 / 900);
        let height = gameCanvas.paddle1Height;
        let width = gameCanvas.canvas.height * 25 / 900;
        let deltaY = y * gameCanvas.canvas.height - height / 2;

        // Ajuster les coordonnées pour éviter les imprécisions
        x = Math.floor(x);
        deltaY = Math.floor(deltaY);
        width = Math.round(width);
        height = Math.round(height);

        gameCanvas.ctx.drawImage(imgPaddleL.canvas, x, deltaY, width, height);
    }
}

function drawBallXY(x, y) {
    var ballX = x * gameCanvas.canvas.width;
    var ballY = y * gameCanvas.canvas.height;

    // Assurez-vous que l'image est chargée avant de la dessiner
    if (imgBall.complete) {
        gameCanvas.ctx.save();
        gameCanvas.ctx.beginPath();
        gameCanvas.ctx.arc(ballX, ballY, gameCanvas.ballRadius, 0, Math.PI * 2);
        gameCanvas.ctx.clip();
        gameCanvas.ctx.drawImage(imgBall, ballX - gameCanvas.ballRadius, ballY - gameCanvas.ballRadius, gameCanvas.ballRadius * 2, gameCanvas.ballRadius * 2);
        gameCanvas.ctx.restore();
    }
}

function drawPowerup(y) {
    // 600 - taille du powerup / 2
    var powerupX = gameCanvas.canvas.width * (600 - gameCanvas.powerupsize * 900 / 2) / 1200;
    var powerupY = (y - gameCanvas.powerupsize / 2) * gameCanvas.canvas.height;

    // Assurez-vous que l'image est chargée avant de la dessiner
    if (imgPowerUp.complete) {
        gameCanvas.ctx.save();
        gameCanvas.ctx.beginPath();
        gameCanvas.ctx.rect(powerupX, powerupY, gameCanvas.canvas.height * gameCanvas.powerupsize, gameCanvas.canvas.height * gameCanvas.powerupsize);
        gameCanvas.ctx.clip();
        gameCanvas.ctx.drawImage(imgPowerUp, powerupX, powerupY, (gameCanvas.canvas.height - 50) * gameCanvas.powerupsize, (gameCanvas.canvas.height - 50) * gameCanvas.powerupsize);
        gameCanvas.ctx.restore();
    }
}

function drawVerticalDashedBorder() {
    var middleX = gameCanvas.canvas.width / 2;
    gameCanvas.ctx.setLineDash([7, 4]); // Dash of 7 pixels, gap of 4 pixels
    gameCanvas.ctx.lineWidth = 2;
    gameCanvas.ctx.strokeStyle = 'white';
    gameCanvas.ctx.beginPath();
    gameCanvas.ctx.moveTo(middleX, 0); // Start at the top middle of the canvas
    gameCanvas.ctx.lineTo(middleX, gameCanvas.canvas.height); // End at the bottom middle of the canvas
    gameCanvas.ctx.stroke();
    gameCanvas.ctx.setLineDash([]); // Reset to solid line for other drawings
}

function drawImpactAnimation(x, y) {
    var radius = 100; // initial radius of the circle
    var alpha = 1.0; // initial opacity

    // Define animation loop
    function animate() {

        // Draw circle
        gameCanvas.ctx.beginPath();
        gameCanvas.ctx.arc(x, y, radius, 0, Math.PI * 2);
        gameCanvas.ctx.fillStyle = 'rgba(255, 255, 255, ' + alpha + ')';
        gameCanvas.ctx.fill();

        // Update parameters
        alpha -= 0.02; // decrease opacity
        radius += 10; // increase radius for effect

        // Stop animation when opacity is too low
        if (alpha > 0) {
            requestAnimationFrame(animate);
        }
    }

    animate(); // Start animation
}

function draw(data) {
    gameCanvas.ctx.clearRect(0, 0, gameCanvas.canvas.width, gameCanvas.canvas.height);
    drawVerticalDashedBorder();
    drawPaddleR(data.paddleR);
    drawPaddleL(data.paddleL);
    drawBallXY(data.ballX, data.ballY);
	if (gameCanvas.powerup)
    	drawPowerup(data.powerupY);
    if (data.ballX < 0.01 && gameCanvas.inGame == true) {
        drawImpactAnimation(0, data.ballY * gameCanvas.canvas.height);
    } else if (data.ballX > 0.99 && gameCanvas.inGame == true) {
        drawImpactAnimation(gameCanvas.canvas.width, data.ballY * gameCanvas.canvas.height);
    }
}

