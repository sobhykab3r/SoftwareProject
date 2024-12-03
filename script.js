document.addEventListener('DOMContentLoaded', (event) => {
    const signInBtn = document.getElementById('signInBtn');
    const modal = document.getElementById('signInModal');
    const closeBtn = document.querySelector('.close');

    signInBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});
