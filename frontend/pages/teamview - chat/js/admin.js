// --- Admin-Rechte übertragen ---
const checkbox = document.querySelector('.confirmation-checkbox');
const transferButton = document.querySelector('.transfer-button');

if (checkbox && transferButton) {
    checkbox.addEventListener('change', function () {
        transferButton.disabled = !this.checked;
    });
}

// --- Wortfilter: Wörter hinzufügen/entfernen ---
const addBtn = document.querySelector('.add-word-button');
const input = document.querySelector('.word-input');
const list = document.querySelector('.word-list');

if (addBtn && input && list) {
    addBtn.addEventListener('click', () => {
        const word = input.value.trim();
        if (!word) return;

        const li = document.createElement('li');
        li.classList.add('word-item');
        li.innerHTML = `
            <span>${word}</span>
            <button class="remove-word-button">Entfernen</button>
        `;

        list.appendChild(li);
        input.value = "";
    });

    list.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-word-button')) {
            e.target.parentElement.remove();
        }
    });
}
