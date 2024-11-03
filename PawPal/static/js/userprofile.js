document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profileForm');
    const modal = document.getElementById('updateModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const modalCloseButton = document.getElementById('modalCloseButton');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modalTitle.textContent = 'Success';
                modalMessage.textContent = 'Your profile has been updated successfully.';
            } else {
                modalTitle.textContent = 'Error';
                modalMessage.textContent = data.error || 'An error occurred while updating your profile.';
            }
            modal.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            modalTitle.textContent = 'Success';
            modalMessage.textContent = 'Profile updated successfully!';
            modal.classList.remove('hidden');
        });
    });

    modalCloseButton.addEventListener('click', function() {
        modal.classList.add('hidden');
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });
});