// Recherche un utilisateur
async function searchUser(input, suggestionList) {
  if (!input || !suggestionList) {
    return;
  }
  
  suggestionList.addEventListener('click', (e) => {
    if (e.target.tagName === 'LI') {
      input.value = e.target.textContent.replace('👤 ', '');
      suggestionList.classList.add('hidden');
    }
  });
  
  input.addEventListener('input', async (e) => {
    const value = e.target.value;
    if (value.length < 3) {
      suggestionList.classList.add('hidden');
      return;
    }
  
    const response = await fetch(`../search-users?search=${value}`);
    const data = await response.json();
    const users = data.users;
  
    if (!suggestionList) return;
  
    if (users.length === 0 || value.length === 0) {
      suggestionList.classList.add('hidden');
    } else {
      suggestionList.classList.remove('hidden');
    }
  
    suggestionList.innerHTML = '';
    users.forEach((user) => {
      const li = document.createElement('li');
      li.textContent = "👤 " + user.username;
      suggestionList.appendChild(li);
    });
  });
}


document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-username');
  const suggestionList = document.getElementById('users-suggestions-list');
  searchUser(input, suggestionList);
});

