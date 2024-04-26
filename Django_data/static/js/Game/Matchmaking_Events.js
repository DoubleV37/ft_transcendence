function matchmaking_SetEvents() {

	// Fonction pour se connecter au WebSocket
	gameSocket = new WebSocket("wss://" + window.location.host + "/wss/game/matchmaking");

	gameSocket.onopen = function(event) {
		console.log('WebSocket connection established.');
		gameSocket.send('search');
		addDot();
	};
	
	gameSocket.onmessage = function(event) {
		console.log('Message received from server:', event.data);
		data = JSON.parse(event.data);
		if (data.type == "match_found") {
			console.log('Match found:', data);
			gameSocket.close();
			loadPage(`${ROUTE.GAME_ROOM}${data.room_name}/`);
		}
	};
	
	gameSocket.onerror = function(error) {
		console.error('WebSocket error:', error);
	};
	
	gameSocket.onclose = function(event) {
		console.log('WebSocket connection closed:', event);
	};
	
}

function matchmaking_DelEvents() {
	gameSocket.close();
}

function addDot() {
	
	console.log("DOT=", dots);
	const titleElement = document.getElementById('matchmakingDots');
	
	if (dots < 3) {
		titleElement.textContent += '.';
		dots++;
	} else {
		titleElement.textContent = titleElement.textContent.slice(0, -3);
		dots = 0;
	}
	setTimeout(addDot, 500);
}

