function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function addPokemonToTeam(team, pokemonId, teamId) {
    const url = `/team/` + teamId + `/`;
    const csrfToken = getCookie('csrftoken');

    var teamData = team;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ pokemonId: pokemonId })
    })
    .then(data => {
        console.log(data);
        window.location.reload();
    })
    .catch(error => console.error('Erreur:', error));
}