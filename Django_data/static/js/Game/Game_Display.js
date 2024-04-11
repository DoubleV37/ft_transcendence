function drawPaddleR(y) {
    if (imgPaddleR.isInitialized()) {
        // Calculer les coordonnées exactes pour le dessin du paddle droit
        let x = canvas.width - (canvas.width * 50 / 1200) - (canvas.height * 25 / 900) + (canvas.height * 25 / 900); // Prend en compte la largeur du paddle
        let height = paddle2Height;
        let width = canvas.height * 25 / 900;
        let deltaY = y * canvas.height - height / 2;
        
        // Ajuster les coordonnées pour éviter les imprécisions
        x = Math.floor(x);
        deltaY = Math.floor(deltaY);
        width = Math.round(width);
        height = Math.round(height);
        
        ctx.drawImage(imgPaddleR.canvas, x, deltaY, width, height);
    }
}

function drawPaddleL(y) {
    if (imgPaddleL.isInitialized()) {
        // Calculer les coordonnées exactes pour le dessin du paddle gauche
        let x = (canvas.width * 50 / 1200) - (canvas.height * 25 / 900);
        let height = paddle1Height;
        let width = canvas.height * 25 / 900;
        let deltaY = y * canvas.height - height / 2;
        
        // Ajuster les coordonnées pour éviter les imprécisions
        x = Math.floor(x);
        deltaY = Math.floor(deltaY);
        width = Math.round(width);
        height = Math.round(height);
        
        ctx.drawImage(imgPaddleL.canvas, x, deltaY, width, height);
    }
}

function drawBallXY(x, y, imgBall) {
    var ballX = x * canvas.width;
    var ballY = y * canvas.height;
    
    // Assurez-vous que l'image est chargée avant de la dessiner
    if (imgBall.complete) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(imgBall, ballX - ballRadius, ballY - ballRadius, ballRadius * 2, ballRadius * 2);
        ctx.restore();
    }
}

function drawPowerup(y, imgPowerUp) {
    // 600 - taille du powerup / 2
    var powerupX = canvas.width * (600 - powerupsize * 900 / 2) / 1200;
    var powerupY = (y - powerupsize / 2) * canvas.height;
    
    // Assurez-vous que l'image est chargée avant de la dessiner
    if (imgPowerUp.complete) {
        ctx.save();
        ctx.beginPath();
        ctx.rect(powerupX, powerupY, canvas.height * powerupsize, canvas.height * powerupsize);
        ctx.clip();
        ctx.drawImage(imgPowerUp, powerupX, powerupY, (canvas.height - 50) * powerupsize, (canvas.height - 50) * powerupsize);
        ctx.restore();
    }
}

function drawVerticalDashedBorder() {
    var middleX = canvas.width / 2;
    ctx.setLineDash([7, 4]); // Dash of 7 pixels, gap of 4 pixels
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'white';
    ctx.beginPath();
    ctx.moveTo(middleX, 0); // Start at the top middle of the canvas
    ctx.lineTo(middleX, canvas.height); // End at the bottom middle of the canvas
    ctx.stroke();
    ctx.setLineDash([]); // Reset to solid line for other drawings
}

function drawImpactAnimation(x, y) {
    var radius = 100; // initial radius of the circle
    var alpha = 1.0; // initial opacity
    
    // Define animation loop
    function animate() {
        
        // Draw circle
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, ' + alpha + ')';
        ctx.fill();
        
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
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawVerticalDashedBorder();
    drawPaddleR(data.paddleR);
    drawPaddleL(data.paddleL);
    drawBallXY(data.ballX, data.ballY, imgBall);
    drawPowerup(data.powerupY, imgPowerUp);
    if (data.ballX < 0.01) {
        drawImpactAnimation(0, data.ballY * canvas.height);
    } else if (data.ballX > 0.99) {
        drawImpactAnimation(canvas.width, data.ballY * canvas.height);
    }
}

