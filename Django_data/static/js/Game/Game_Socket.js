function init_websocket() {
	// Create WebSocket connection.
	gameSocket.onopen = function (e) {
		console.log("The connection was setup successfully !");
	};
	gameSocket.onclose = function (e) {
		console.log("Something unexpected happened !");
	};
}

// function receive_data(e) {
// 	const data = JSON.parse(e.data);
// 	let score1div = document.getElementById("score1div");
// 	score1div.innerHTML = data.score1;
// 	let score2div = document.getElementById("score2div");
// 	score2div.innerHTML = data.score2;
// 	gameCanvas.ballRadius = data.ballsize * gameCanvas.height*2;
// 	gameCanvas.paddle1Height = data.paddle1size * gameCanvas.height;
// 	gameCanvas.paddle2Height = data.paddle2size * gameCanvas.height;
// 	gameCanvas.powerupY = data.powerupY;
// 	gameCanvas.powerupsize = data.powerupsize;
// 	draw(data);
// }

function receive_data_room(e) {
	const data = JSON.parse(e.data);
	if (data.message === "opponent") {
		gameCanvas.opponent = data.opponent;
		gameCanvas.num = data.num;
		return;
	}
	if (data.message === "User exited") {
		console.log("User exited");
		alert("The opponent ran away in fear!");
		gameSocket.send(JSON.stringify({ message: "stop" }));
	}
	if (data.message === "Game stopped") {
		alert("Game stopped!");
		gameSocket.close();
		loadPage(ROUTE.GAME_MODES);
	}
	if (data.message === "win") {
		alert("You won!");
		gameSocket.close();
		loadPage(ROUTE.GAME_MODES);
	}
	if (data.message === "lose") {
		alert("You lost!");
		gameSocket.close();
		loadPage(ROUTE.GAME_MODES);
	}
	if (data.message === "game_state") {
		let score1div = document.getElementById("score1div");
		let score2div = document.getElementById("score2div");
		score1div.innerHTML = data.score1;
		score2div.innerHTML = data.score2;
		gameCanvas.ballRadius = data.ballsize*gameCanvas.height*2;
		gameCanvas.paddle1Height = data.paddle1size*gameCanvas.height;
		gameCanvas.paddle2Height = data.paddle2size*gameCanvas.height;
		draw(data);
	}
}

function sendMovement(direction) {
	gameSocket.send(JSON.stringify({ message: direction }));
}

// Fonction pour mettre à jour le mouvement en fonction du temps écoulé
function update() {
	if (keyStates['ArrowUp']) {
		sendMovement("up");
	}
	else if (keyStates['ArrowDown']) {
		sendMovement("down");
	}
	else if (keyStates[' ']) {
		sendMovement("space");
	}
	if (keyStates['w']) {
		sendMovement("w");
	}
	else if (keyStates['s']) {
		sendMovement("s");
	}
	// Planifiez la prochaine mise à jour
	requestAnimationFrame(update);
}

