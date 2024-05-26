document.addEventListener('DOMContentLoaded', function () {
    loadFilters();
    fetchBooks(true);

    document.getElementById('filter-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetchBooks(true);
    });

    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetchBooks(true);
    });

    document.getElementById('order-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetchBooks(true);
    });
});

function loadFilters() {
    fetch('/api/authors/')
        .then(response => response.json())
        .then(data => {
            const authorFilter = document.getElementById('author-filter');
            data.results.forEach(author => {
                const option = document.createElement('option');
                option.value = author.id;
                option.textContent = author.name;
                authorFilter.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching authors:', error));

    fetch('/api/genres/')
        .then(response => response.json())
        .then(data => {
            const genreFilter = document.getElementById('genre-filter');
            data.results.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre.id;
                option.textContent = genre.name;
                genreFilter.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching genres:', error));
}

function fetchBooks(filters_needed, url = '/api/books/') {
    const urlParams = new URLSearchParams();
    const searchQuery = document.getElementById('search-query').value;
    const authorFilter = document.getElementById('author-filter').value;
    const genreFilter = document.getElementById('genre-filter').value;
    const ordering = document.getElementById('ordering').value;

    if (filters_needed) {
        if (searchQuery) {
            urlParams.set('search', searchQuery);
        }
        if (authorFilter) {
            urlParams.set('author', authorFilter);
        }
        if (genreFilter) {
            urlParams.set('genres', genreFilter);
        }
        if (ordering) {
            urlParams.set('ordering', ordering);
        }

        const queryString = urlParams.toString();

        if (queryString) {
            url += (url.includes('?') ? '&' : '?') + queryString;
        }
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderBooks(data.results);
            renderPagination(data);
        })
        .catch(error => console.error('Error fetching books:', error));
}

function renderBooks(books) {
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = '';
    books.forEach(book => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>
                <a href="/book-list/${book.id}/">${book.title}</a> by ${book.author_name}
            </span>
            <span>
                <a class="btn btn-reserve" href="/book-list/${book.id}/">Reserve</a>
            </span>`;
        bookList.appendChild(li);
    });
}

function renderPagination(data) {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';

    if (data.previous) {
        const firstPageLink = createPageLink('First', '/api/books/?page=1', true);
        paginationContainer.appendChild(firstPageLink);

        const prevPageLink = createPageLink('Previous', data.previous, false);
        paginationContainer.appendChild(prevPageLink);
    }

    const currentPageSpan = document.createElement('span');
    currentPageSpan.classList.add('current');
    currentPageSpan.textContent = data.current;
    paginationContainer.appendChild(currentPageSpan);

    if (data.next) {
        const nextPageLink = createPageLink('Next', data.next, false);
        paginationContainer.appendChild(nextPageLink);

        const lastPageLink = createPageLink('Last', `/api/books/?page=${data.last_page}`, true);
        paginationContainer.appendChild(lastPageLink);
    }
}

function createPageLink(text, url, filters_needed) {
    const link = document.createElement('a');
    link.href = 'javascript:void(0)';
    link.textContent = text;
    link.addEventListener('click', function() {
        fetchBooks(filters_needed, url);
    });
    return link;
}
