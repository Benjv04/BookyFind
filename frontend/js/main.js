const deeplApiKey = '915ad76d-feb6-41c6-a71a-d43874236a92:fx'; // Reemplaza con tu clave real de DeepL


// para que no deje modificar el url que no sean lo base
document.addEventListener("DOMContentLoaded", function () {
    const esLocal = window.location.protocol === "file:";
    if (esLocal) return; // No aplicar redirección si estás trabajando con archivos locales

    const paginasPermitidas = ["/", "/index.html", "/contacto.html", "/libros.html", "/carrito.html", "/clubes.html", "/ofertas.html"];
    const pathname = window.location.pathname;

    if (!paginasPermitidas.includes(pathname)) {
        window.location.href = "/index.html";
    }
});

// 🔹 Función para traducir texto con DeepL
async function translateText(text, targetLang = 'ES') {
    if (!text || text.trim() === '') return 'Sin descripción disponible';

    try {
        const response = await fetch('https://api-free.deepl.com/v2/translate', {
            method: 'POST',
            headers: {
                'Authorization': `DeepL-Auth-Key ${deeplApiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: [text.substring(0, 500)],
                target_lang: targetLang
            })
        });

        if (!response.ok) {
            console.error(`Error en la respuesta de DeepL: ${response.status}`);
            return text;
        }

        const data = await response.json();
        return data.translations[0].text || text;
    } catch (error) {
        console.error('❌ Error en la traducción con DeepL:', error);
        return text;
    }
}

// 🔹 API del New York Times
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
                const translatedTitle = await translateText(book.title);
                const translatedDesc = await translateText(book.description || '');

                const bookCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="${book.book_image}" class="card-img-top" alt="${book.title}">
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${translatedTitle}</h5>
                                <p class="card-text">${translatedDesc}</p>
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

// 🔹 Cálculo del total del carrito
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
