let currentPopup = null;

function showPopup(pokemonId) {
	if (currentPopup) {
		currentPopup.style.display = "none";
	}

	const popup = document.getElementById(`popup-${pokemonId}`);
	popup.style.display = "block";
	currentPopup = popup;
}

function hidePopup(pokemonId) {
	const popup = document.getElementById(`popup-${pokemonId}`);
	popup.style.display = "none";
	currentPopup = null;
}