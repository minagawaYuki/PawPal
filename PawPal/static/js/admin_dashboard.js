document.addEventListener('DOMContentLoaded', function() {
    const confirmationModal = document.getElementById('confirmationModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const confirmButton = document.getElementById('confirmButton');
    const cancelButton = document.getElementById('cancelButton');
    const actionButtons = document.querySelectorAll('.accept-button, .delete-button, .finish-button');

    const messageModal = document.getElementById('messageModal');
    const messageTitle = document.getElementById('messageTitle');
    const messageContent = document.getElementById('messageContent');
    const messageCloseButton = document.getElementById('messageCloseButton');

    let currentAction = '';
    let currentBookingId = '';

    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            currentAction = button.dataset.action;
            currentBookingId = button.dataset.bookingId;
            openConfirmationModal();
        });
    });

    function openConfirmationModal() {
        let actionString, colorClass;
        switch(currentAction) {
            case 'accept':
                actionString = 'Accept';
                colorClass = 'bg-green-500 hover:bg-green-600';
                break;
            case 'delete':
                actionString = 'Delete';
                colorClass = 'bg-red-500 hover:bg-red-600';
                break;
            case 'finish':
                actionString = 'Finish';
                colorClass = 'bg-blue-500 hover:bg-blue-600';
                break;
        }
        
        modalTitle.textContent = `${actionString} Booking`;
        modalMessage.textContent = `Are you sure you want to ${currentAction} this booking?`;
        confirmButton.textContent = actionString;
        confirmButton.className = `px-4 py-2 text-white font-semibold rounded transition-colors ${colorClass}`;
        confirmationModal.classList.remove('hidden');
    }

    function closeConfirmationModal() {
        confirmationModal.classList.add('hidden');
    }

    confirmButton.addEventListener('click', () => {
        updateBookingStatus(currentBookingId, currentAction);
        closeConfirmationModal();
    });

    cancelButton.addEventListener('click', closeConfirmationModal);

    window.addEventListener('click', (event) => {
        if (event.target === confirmationModal) {
            closeConfirmationModal();
        }
    });

    function updateBookingStatus(bookingId, action) {
        const url = `/admindashboard/bookings/${action}/`;
        
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ booking_id: bookingId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let actionString = action === 'accept' ? 'accepted' : 
                                   action === 'finish' ? 'finished' : 'deleted';
                showMessage('Success', `Booking ${actionString} successfully!`);
                updateUI(bookingId, action);
            } else {
                showMessage('Error', data.error || "An error occurred.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showMessage('Error', "An unexpected error occurred.");
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateUI(bookingId, action) {
        const row = document.querySelector(`[data-booking-id="${bookingId}"]`).closest('tr');
        if (action === 'delete') {
            row.remove();
        } else {
            const statusCell = row.querySelector('td:last-child');
            statusCell.textContent = action === 'accept' ? 'Accepted' : 'Finished';
        }
    }

    function showMessage(title, message) {
        messageTitle.textContent = title;
        messageContent.textContent = message;
        messageModal.classList.remove('hidden');
    }

    function closeMessageModal() {
        messageModal.classList.add('hidden');
    }

    messageCloseButton.addEventListener('click', closeMessageModal);

    window.addEventListener('click', (event) => {
        if (event.target === messageModal) {
            closeMessageModal();
        }
    });
});