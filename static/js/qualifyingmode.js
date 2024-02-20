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

// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('submitLapTimes').addEventListener('click', function() {
//         const lapTimeInputs = document.querySelectorAll('.lap-time');
//         lapTimeInputs.forEach(input => {
//             const racerId = input.getAttribute('data-racer-id');
//             const lapNumber = input.getAttribute('data-lap-number');
//             const lapTime = input.value;

//             // Regular expression to match the MM:SS.SSS format
//             const lapTimeFormat = /^\d{2}:\d{2}\.\d{3}$/;

//             if (lapTime && lapTimeFormat.test(lapTime)) {  // Check if there's a value and it matches the format
//                 fetch('/save-lap-times/', {  // Update with the correct URL
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': getCookie('csrftoken'),  // Function to get CSRF token
//                     },
//                     body: JSON.stringify({racerId, lapNumber, lapTime}),
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log('Success:', data);
//                 })
//                 .catch((error) => {
//                     console.error('Error:', error);
//                 });
//             } else if (lapTime && !lapTimeFormat.test(lapTime)) {
//                 console.error('Error: Lap time format is incorrect. It should be MM:SS.SSS.');
//                 alert('Lap time format is incorrect. Please use MM:SS.SSS format.'); // Optionally alert the user
//             }
//         });
//     });
// });

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
