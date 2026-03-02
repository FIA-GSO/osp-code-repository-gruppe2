const groupId = "c6d25d09-fbbd-4492-a03e-10621a3319e9"; // Hier echte Gruppen-ID einsetzen
let currentUserRole = null;

async function loadData() {
    const response = await fetch(`/api/groups/${groupId}`);
    const data = await response.json();
    currentUserRole = data.currentUserRole;
    renderMembers(data.members);
    renderRequests(data.requests);
}

function renderMembers(members) {
    const list = document.querySelector(".member-list");
    list.innerHTML = "";
    members.forEach(member => {
        let roleBadge = `<span class="tag-5">${member.role}</span>`;
        let deleteIcon = "";
        if ((currentUserRole === "OWNER" || currentUserRole === "ADMIN") && member.role !== "OWNER") {
            deleteIcon = `<span class="delete-forever-icon-1" onclick="deleteMember('${member.id}')">🗑️</span>`;
        }
        list.innerHTML += `
        <div class="member-card">
          <span class="account-circle-icon-2">👤</span>
          <a href="#">${member.first_name} ${member.last_name}</a>
          ${roleBadge}
          ${deleteIcon}
        </div>`;
    });
    document.querySelector(".anzahl-4").textContent = "Anzahl: " + members.length;
}

async function deleteMember(userId) {
    await fetch(`/api/groups/${groupId}/members/${userId}`, { method: "DELETE" });
    loadData();
}

function renderRequests(requests) {
    const section = document.querySelector(".requests-section");
    section.innerHTML = `<h3 class="anfragen">Anfragen</h3>`;
    requests.forEach(user => {
        section.innerHTML += `
        <div class="member-card">
          <span class="account-circle-icon-6">👤</span>
          <a href="#">${user.first_name} ${user.last_name}</a>
          <span class="check-circle-icon-1" onclick="acceptRequest('${user.id}')">✔️</span>
          <span class="delete-forever-icon-5">🗑️</span>
        </div>`;
    });
}

async function acceptRequest(userId) {
    await fetch(`/api/groups/${groupId}/invitations/${userId}/accept`, { method: "POST" });
    loadData();
}




