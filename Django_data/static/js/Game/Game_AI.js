
function iaBrain (data) {
	const rand = Math.floor(Math.random() * 81) - 40;
	let bx = data.ballX * 1200;
	let by = data.ballY * 900;
	const sx = data.ballspeedX;
	let sy = data.ballspeedY;
	iaMemory.pos = data.paddleL * 900;

	if (sx === 0) {
		iaMemory.target = Math.floor(Math.random() * 301) + 300;
		if (bx < 600) {
		iaMemory.service = true;
		}
	} else if (sx > 0) {
		iaMemory.target = 450;
	} else {
		while (bx > 60) {
		bx += sx;
		by += sy;
		if (by < 5 || by > 895) {
			sy *= -1;
		}
		}
		iaMemory.target = by + rand;
	}
}
  
function iaMove () {
	if (iaMemory.pos < iaMemory.target - 10) {
		gameSocket.send(JSON.stringify({ message: "s" }));
		iaMemory.pos += iaMemory.step;
	} else if (iaMemory.pos > iaMemory.target + 10) {
		gameSocket.send(JSON.stringify({ message: "w" }));
		iaMemory.pos -= iaMemory.step;
	} else if (iaMemory.service) {
		gameSocket.send(JSON.stringify({ message: "space" }));
		iaMemory.service = false;
	}
}