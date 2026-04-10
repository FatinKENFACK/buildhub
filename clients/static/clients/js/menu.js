document.querySelectorAll('.option').forEach(item =>{
    item.addEventListener('click', () => {
        document.getElementById('selected-label').textContent = item.dataset.value;
        document.getElementById('selected-label').classList.remove('text-blue-500');
        document.getElementById('menu').classList.add('hidden');
        document.getElementById('arrow').classList.remove('rotate-100');
    });
});

// fermer en cliquant en dehors

document.addEventListener('click', e => {
    if (!e.target.closest('#dropdown')) {
        document.getElementById('menu').classList.add('hidden');
        document.getElementById('arrow').classList.remove('rotate-180');
    }
});