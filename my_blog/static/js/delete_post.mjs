document.getElementById('delete-form').addEventListener('submit', function (event) {
    const confirmed = confirm('Êtes-vous sûr de supprimer définitivement ce post ?');
    if (!confirmed) {
        event.preventDefault();
    }
});