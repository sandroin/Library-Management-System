document.addEventListener('DOMContentLoaded', function() {
    const bookId = window.location.pathname.split('/').slice(-2, -1)[0];

    fetch(`/api/books/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('book-title').textContent = data.title;
            document.getElementById('book-author').textContent = data.author_name;
            document.getElementById('book-genres').textContent = data.genres.join(', ');
            document.getElementById('book-publication-date').textContent = data.publication_date;
            const quantity = data.available_quantity;
            document.getElementById('book-availability').textContent = quantity > 0 ? 'Available' : 'Not Available';
            document.getElementById('reserve-or-wish').textContent = quantity > 0 ? 'Reserve' : 'Add to Wishlist';

            document.getElementById('reserveButton').addEventListener('click', function() {
                const csrftoken = document.cookie.split('; ')
                    .find(cookie => cookie.startsWith('csrftoken='))
                    .split('=')[1];

                fetch('/api/reservations/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ book_id: bookId })
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/book-list/';
                    } else {
                        return response.json().then(data => {
                            alert('Error: ' + (data.error || 'Unknown error occurred'));
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        })
        .catch(error => {
            console.error('Error fetching book data:', error);
        });
});