// overview.js – gemeinsam für my-teams und erkunden

const JOIN_POLICY_LABELS = {
    open:   "Frei beitreten",
    invite: "Nur per Einladung",
    closed: "Geschlossen",
};

const PLACEHOLDER_COLORS = ["image-placeholder-1", "image-placeholder-2", "image-placeholder-3"];

function erstelleKarte(gruppe, index, modus) {
    const colorClass = PLACEHOLDER_COLORS[index % PLACEHOLDER_COLORS.length];
    const linkClass  = `link-${(index % 3) + 1}`;
    const flagClass  = `flag-icon-${(index % 3) + 1}`;

    let buttonLabel, btnClass;
    if (modus === "explore") {
        buttonLabel = gruppe.join_policy === "open" ? "Beitreten" : "Beitritt anfragen";
        btnClass    = gruppe.join_policy === "open" ? "button-1" : "button-4";
    } else {
        buttonLabel = "Öffnen";
        btnClass    = "button-1";
    }

    return `
    <article class="card">
        <div class="card-header">
            <div class="${colorClass}">
                <svg viewBox="0 0 24 24"><path d="M14 6l-3.75 5 2.85 3.8-1.6 1.2C9.81 13.75 7 10 7 10l-6 8h22L14 6z"/></svg>
            </div>
            <div class="card-title-group">
                <span class="team-label">Team:</span>
                <a href="#" class="${linkClass}">${gruppe.name}</a>
            </div>
        </div>

        <div class="card-description">
            ${gruppe.description ? `<p>${gruppe.description}</p>` : ""}
            <small>Max. ${gruppe.max_members || "–"} Mitglieder · ${JOIN_POLICY_LABELS[gruppe.join_policy] || gruppe.join_policy}</small>
        </div>

        <div class="card-actions">
            <button class="${btnClass}">${buttonLabel}</button>
            <svg class="${flagClass}" viewBox="0 0 24 24">
                <path d="M14.4 6L14 4H5v17h2v-7h5.6l.4 2h7V6z"/>
            </svg>
        </div>
    </article>`;
}

function zeigeLeerzustand(modus) {
    const text = modus === "explore"
        ? "Keine Gruppen gefunden."
        : "Du bist noch in keiner Gruppe.";
    const sub = modus === "explore"
        ? "Erstelle eine neue Gruppe oder schau später nochmal vorbei."
        : "Erstelle eine neue Gruppe oder tritt einer bei.";

    return `
    <div class="empty-state">
        <svg viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
        <p>${text}</p>
        <small>${sub}</small>
    </div>`;
}

async function ladeGruppen() {
    const container = document.getElementById("cardsContainer");
    const modus     = container.dataset.modus; // "mine" oder "explore"
    const url       = modus === "explore" ? "/groups/api/explore" : "/groups/api/mine";

    try {
        const response = await fetch(url);

        if (!response.ok) throw new Error(`Status: ${response.status}`);

        const gruppen = await response.json();

        container.innerHTML = gruppen.length === 0
            ? zeigeLeerzustand(modus)
            : gruppen.map((g, i) => erstelleKarte(g, i, modus)).join("");

    } catch (err) {
        console.error("Fehler beim Laden der Gruppen:", err);
        container.innerHTML = zeigeLeerzustand(modus);
    }
}

ladeGruppen();