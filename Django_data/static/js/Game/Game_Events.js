addEventListener('resize', () => {
    style = getComputedStyle(canvas);
    width = parseInt(style.getPropertyValue('width'), 10);
    height = parseInt(style.getPropertyValue('height'), 10);
    canvas.width = width;
    canvas.height = height;
});

// Clear key states on keyup
document.addEventListener('keyup', function(e) {
    keyStates[e.key] = false;
});

// Set key states on keydown
document.addEventListener('keydown', function(e) {
    if (e.key !== 'F5' && !(e.key === 'F5' && e.ctrlKey) && e.key !== 'F12') {
        e.preventDefault();
    }
    keyStates[e.key] = true;
});
