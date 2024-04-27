function keyUp (e) {
	keyStates[e.key] = false;
}

function keyDown (e) {
	if (e.key !== "F5" && !(e.key === "F5" && e.ctrlKey) && e.key !== "F12") {
	e.preventDefault();
	}
	keyStates[e.key] = true;
}

function init_canvas () {
	gameCanvas.canvas = document.getElementById("MyCanvas");
	gameCanvas.ctx = gameCanvas.canvas.getContext("2d");
	gameCanvas.style = getComputedStyle(gameCanvas.canvas);
	gameCanvas.width = parseInt(gameCanvas.style.getPropertyValue("width"), 10);
	gameCanvas.height = parseInt(gameCanvas.style.getPropertyValue("height"), 10);
	gameCanvas.canvas.width = gameCanvas.width;
	gameCanvas.canvas.height = gameCanvas.height;
}

function game_SetEvents (page_name) {
	// addEventListener('resize', () => {
	// 	style = getComputedStyle(canvas);
	// 	width = parseInt(style.getPropertyValue('width'), 10);
	// 	height = parseInt(style.getPropertyValue('height'), 10);
	// 	canvas.width = width;
	// 	canvas.height = height;
	// });
	gameStop = false;
	gameSocket = new WebSocket("wss://" + window.location.host + "/wss" + window.location.pathname);
	gameSocket.addEventListener("open", OpenTest);
	gameSocket.addEventListener("close", CloseTest);
	init_canvas();
}

function OpenTest () {
	console.log("The connection was setup successfully !");
	if (window.location.pathname === "/game/solo/") {
		console.log(GameParams);
		gameCanvas.powerup = GameParams.powerup;
		gameSocket.send(JSON.stringify(GameParams));
	} else {
		gameCanvas.powerup = false;
		GameParams.point_limit = 1;
		GameParams.type = "remote";
		GameParams.opponent = "player";
		gameSocket.send(JSON.stringify(GameParams));
	}

	gameSocket.addEventListener("message", receive_data);
	document.addEventListener("keyup", keyUp);
	document.addEventListener("keydown", keyDown);

	update();
}

function CloseTest () {
	gameSocket.removeEventListener("message", receive_data);
	gameSocket.removeEventListener("open", OpenTest);
	gameSocket.removeEventListener("close", CloseTest);

	console.log("Socket was closed!");
	gameSocket = null;
	gameStop = true;
}

function game_DelEvents() {
	console.log('game_DelEvents');
	if (gameSocket.readyState === WebSocket.OPEN)
		gameSocket.send(JSON.stringify({ message: "stop"}));
	// removeEventListener('resize', () => {
		// 	style = getComputedStyle(canvas);
		// 	width = parseInt(style.getPropertyValue('width'), 10);
		// 	height = parseInt(style.getPropertyValue('height'), 10);
		// 	canvas.width = width;
		// 	canvas.height = height;
		// });

	gameSocket.close();

	document.removeEventListener("keyup", keyUp);
	document.removeEventListener("keydown", keyDown);

	keyStates = {
	ArrowUp: false,
	ArrowDown: false,
	w: false,
	s: false,
	space: false
	};
}
