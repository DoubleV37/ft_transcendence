function keyUp(e) {
	keyStates[e.key] = false;
}

function keyDown(e) {
	if (e.key !== 'F5' && !(e.key === 'F5' && e.ctrlKey) && e.key !== 'F12') {
		e.preventDefault();
	}
	keyStates[e.key] = true;
}

function init_canvas() {
	gameCanvas.canvas = document.getElementById("MyCanvas");
	gameCanvas.ctx = gameCanvas.canvas.getContext("2d");
	gameCanvas.style = getComputedStyle(gameCanvas.canvas);
	gameCanvas.width = parseInt(gameCanvas.style.getPropertyValue('width'), 10);
	gameCanvas.height = parseInt(gameCanvas.style.getPropertyValue('height'), 10);
	gameCanvas.canvas.width = gameCanvas.width;
	gameCanvas.canvas.height = gameCanvas.height;
}

function game_SetEvents() {
	// addEventListener('resize', () => {
	// 	style = getComputedStyle(canvas);
	// 	width = parseInt(style.getPropertyValue('width'), 10);
	// 	height = parseInt(style.getPropertyValue('height'), 10);
	// 	canvas.width = width;
	// 	canvas.height = height;
	// });
	gameSocket = new WebSocket("wss://" + window.location.host + "/wss/game/solo");
	init_canvas();
	gameSocket.onopen = function (e) {
		console.log("The connection was setup successfully !");
	};
	gameSocket.onclose = function (e) {
		gameSocket.removeEventListener('message', receive_data);
		console.log("Something unexpected happened !");
	};

	gameSocket.addEventListener('message', receive_data);
	document.addEventListener('keyup', keyUp);
	document.addEventListener('keydown', keyDown);

	update();
}

function game_DelEvents() {
	console.log('game_DelEvents');
	// removeEventListener('resize', () => {
	// 	style = getComputedStyle(canvas);
	// 	width = parseInt(style.getPropertyValue('width'), 10);
	// 	height = parseInt(style.getPropertyValue('height'), 10);
	// 	canvas.width = width;
	// 	canvas.height = height;
	// });

	gameSocket.close();

	document.removeEventListener('keyup', keyUp);

	document.removeEventListener('keydown', keyDown);
}
