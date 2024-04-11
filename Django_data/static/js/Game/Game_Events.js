function keyUp(e) {
	keyStates[e.key] = false;
}

function keyDown(e) {
	if (e.key !== 'F5' && !(e.key === 'F5' && e.ctrlKey) && e.key !== 'F12') {
		e.preventDefault();
	}
	keyStates[e.key] = true;
}

function game_SetEvents() {
	addEventListener('resize', () => {
		style = getComputedStyle(canvas);
		width = parseInt(style.getPropertyValue('width'), 10);
		height = parseInt(style.getPropertyValue('height'), 10);
		canvas.width = width;
		canvas.height = height;
	});

	document.addEventListener('keyup', keyUp);

	document.addEventListener('keydown', keyDown);
}

function game_DelEvents() {
	console.log('game_DelEvents');
	removeEventListener('resize', () => {
		style = getComputedStyle(canvas);
		width = parseInt(style.getPropertyValue('width'), 10);
		height = parseInt(style.getPropertyValue('height'), 10);
		canvas.width = width;
		canvas.height = height;
	});

	document.removeEventListener('keyup', keyUp);

	document.removeEventListener('keydown', keyDown);
}
