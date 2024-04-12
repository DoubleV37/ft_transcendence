function init_websocket() {
	// Create WebSocket connection.
	gameSocket.onopen = function (e) {
		console.log("The connection was setup successfully !");
	};
	gameSocket.onclose = function (e) {
		console.log("Something unexpected happened !");
	};
}

function receive_data(e) {
	const data = JSON.parse(e.data);
	let score1div = document.getElementById("score1div");
	score1div.innerHTML = data.score1;
	let score2div = document.getElementById("score2div");
	score2div.innerHTML = data.score2;
	gameCanvas.ballRadius = data.ballsize * gameCanvas.height*2;
	gameCanvas.paddle1Height = data.paddle1size * gameCanvas.height;
	gameCanvas.paddle2Height = data.paddle2size * gameCanvas.height;
	gameCanvas.powerupY = data.powerupY;
	gameCanvas.powerupsize = data.powerupsize;
	draw(data);
}

function sendMovement(direction) {
	gameSocket.send(JSON.stringify({ message: direction, username: "{{request.user.username}}" }));
}

// Fonction pour mettre à jour le mouvement en fonction du temps écoulé
function update() {
	if (keyStates['ArrowUp']) {
		sendMovement("up");
	} else if (keyStates['ArrowDown']) {
		sendMovement("down");
	}
	else if (keyStates[' '])
		sendMovement("space");
	// Planifiez la prochaine mise à jour
	requestAnimationFrame(update);
}

