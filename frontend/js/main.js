const apiKey = 'wJGxjjL9Z1FT7yfO4LeFpbipiAJqE1iP';
const apiUrl = `https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=${apiKey}`;

async function fetchNYTBooks() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (data && data.results && data.results.books) {
            const books = data.results.books.slice(0, 6); // Muestra solo los primeros 6 libros
            const booksContainer = document.getElementById('nyt-books');
            booksContainer.innerHTML = '';

            for (const book of books) {
                const bookCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="${book.book_image}" class="card-img-top" alt="${book.title}">
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${book.title}</h5>
                                <p class="card-text">${book.description || 'Sin descripción disponible'}</p>
                                <p class="card-text"><strong>Autor:</strong> ${book.author}</p>
                                <a href="${book.amazon_product_url}" target="_blank" class="btn btn-primary mt-auto">Comprar en Amazon</a>
                            </div>
                        </div>
                    </div>
                `;
                booksContainer.innerHTML += bookCard;
            }
        } else {
            console.error('No se encontraron libros en la API del NYT.');
        }
    } catch (error) {
        console.error('Error al obtener los libros del NYT:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchNYTBooks);

function updateTotal() {
    let total = 0;
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const price = parseFloat(row.querySelector('td:nth-child(2)').textContent.replace('$', '').replace('.', ''));
        const quantity = parseInt(row.querySelector('.quantity').textContent);
        total += price * quantity;
    });
    document.querySelector('th[colspan="3"] + th').textContent = `$${total.toLocaleString()}`;
}

// Llama a updateTotal después de cada acción
increaseButtons.forEach(button => {
    button.addEventListener('click', updateTotal);
});
decreaseButtons.forEach(button => {
    button.addEventListener('click', updateTotal);
});
deleteButtons.forEach(button => {
    button.addEventListener('click', updateTotal);
});