let currentPopup = null;

			function showPopup(pokemonId) {
				if (currentPopup) {
					currentPopup.style.display = "none";
				}

				const popup = document.getElementById(`popup-${pokemonId}`);
				popup.style.display = "block";
				currentPopup = popup;

				fetch(`/api/pokemon/${pokemonId}/`)
					.then((response) => response.json())
					.then((data) => {
						console.log(data);
					});
			}

			function hidePopup(pokemonId) {
				const popup = document.getElementById(`popup-${pokemonId}`);
				popup.style.display = "none";
				currentPopup = null;
			}