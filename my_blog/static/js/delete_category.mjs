document.getElementById('delete-form').addEventListener('submit', function (event) {  
    const confirmed = confirm('Êtes-vous sûr de supprimer définitivement cette catégorie ?');
    
    if (!confirmed) {
        event.preventDefault();
    }
});