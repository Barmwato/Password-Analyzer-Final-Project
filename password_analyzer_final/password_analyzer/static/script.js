//Code to move the background image

function moveBackground() {
    const body = document.body;
    const backgroundPosition = parseInt(window.getComputedStyle(body).getPropertyValue("background-position-x"));
    body.style.backgroundPosition = `${backgroundPosition + 1}px 0%`;
    requestAnimationFrame(moveBackground);
}

// Adjust the interval as needed
setInterval(moveBackground, 15550);