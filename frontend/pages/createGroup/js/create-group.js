function handleZurueck(event) {
    if (event) event.preventDefault();

    if (history.length > 1) {
        history.back();
    } else {
        window.location.href = '../../overview/html/my-teams.html';
    }
}

async function gruppeErstellen() {
    const name = document.getElementById('gruppenname').value.trim();
    const maxMitglieder = document.getElementById('maxMitglieder').value;

    if (!name) {
        alert('Bitte einen Gruppennamen eingeben.');
        return;
    }

    if (!maxMitglieder || parseInt(maxMitglieder) < 1) {
        alert('Bitte eine maximale Mitgliederzahl angeben.');
        return;
    }

    const formDaten = new URLSearchParams();
    formDaten.append('name',        name);
    formDaten.append('description', document.getElementById('beschreibung').value.trim());
    formDaten.append('leader_id',   '4349255034b243ae84f10a155f33b786');
    formDaten.append('max_members', maxMitglieder);
    formDaten.append('join_policy', document.querySelector('input[name="access"]:checked').value);

    try {
        const response = await fetch('http://127.0.0.1:5000/groups/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formDaten.toString(),
        });

        if (response.ok || response.redirected) {
            if (history.length > 1) {
                history.back();
            } else {
                window.location.href = '../../overview/html/my-teams.html';
            }
        } else {
            alert(`Fehler beim Erstellen der Gruppe (Status: ${response.status})`);
        }

    } catch (err) {
        console.error('Fehler beim Senden:', err);
        alert('Verbindungsfehler. Bitte erneut versuchen.');
    }
}