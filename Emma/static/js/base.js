let lastClickedButton = null;
function highlightButton(button) {
    if (lastClickedButton) {
        lastClickedButton.style.filter = "brightness(50%)";
    }
    button.style.filter = "brightness(100%)";
    lastClickedButton = button;
}