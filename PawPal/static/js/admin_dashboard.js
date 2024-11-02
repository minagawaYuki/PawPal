document.addEventListener("DOMContentLoaded", function() {
    const acceptButtons = document.querySelectorAll(".accept-button");
    const deleteButtons = document.querySelectorAll(".delete-button");
    const finishButtons = document.querySelectorAll(".finish-button");

    acceptButtons.forEach(button => {
        button.addEventListener("click", function() {
            const bookingId = this.getAttribute("data-booking-id");
            updateBookingStatus(bookingId, "accept");
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            const bookingId = this.getAttribute("data-booking-id");
            updateBookingStatus(bookingId, "delete");
        });
    });

    finishButtons.forEach(button => {
        button.addEventListener("click", function() {
            const bookingId = this.getAttribute("data-booking-id");
            updateBookingStatus(bookingId, "finish");
        });
    });
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
            action_string = ''
            if (action === 'accept') {
                action_string = 'accepted'
            } else if (action === 'finish') {
                action_string = 'finished'
            } else {
                action_string = 'deleted'
            }
            alert(`Booking ${action_string} successfully!`);
        } else {
            alert(data.error || "An error occurred.");
        }
    })
    .catch(error => console.error("Error:", error));
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