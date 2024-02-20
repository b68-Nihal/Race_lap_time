document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitLapTimes').addEventListener('click', function() {
        const lapTimeInputs = document.querySelectorAll('.lap-time');
        lapTimeInputs.forEach(input => {
            const racerId = input.getAttribute('data-racer-id');
            const lapNumber = input.getAttribute('data-lap-number');
            const lapTime = input.value;
            if (lapTime) {  // Only submit if there's a value
                fetch('/save-lap-times/', {  // Update with the correct URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),  // Function to get CSRF token
                    },
                    body: JSON.stringify({racerId, lapNumber, lapTime}),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
