const deeplApiKey = '915ad76d-feb6-41c6-a71a-d43874236a92:fx'; // Reemplaza con tu clave real de DeepL

// 🔹 Función para traducir texto con DeepL
async function translateText(text, targetLang = 'ES') {
    if (!text || text.trim() === '') return 'Sin descripción disponible'; // Evita errores con texto vacío

    try {
        const response = await fetch('https://api-free.deepl.com/v2/translate', {
            method: 'POST',
            headers: {
                'Authorization': `DeepL-Auth-Key ${deeplApiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: [text.substring(0, 500)], // 🔹 DeepL Free tiene un límite de caracteres por solicitud
                target_lang: targetLang
            })
        });

        if (!response.ok) {
            console.error(`Error en la respuesta de DeepL: ${response.status}`);
            return text; // Usa el texto original si hay un error
        }

        const data = await response.json();
        return data.translations[0].text || text; // Devuelve el texto traducido o el original
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
            const books = data.results.books;
            const booksContainer = document.getElementById('nyt-books');
            booksContainer.innerHTML = ''; // Limpia antes de agregar nuevos libros

            for (const book of books) {
                // 🔹 Traduce el título y la descripción
                const translatedTitle = await translateText(book.title);
                const translatedDesc = await translateText(book.description || ''); // Evita fallos con textos vacíos

                const bookCard = `
                    <div class="col-md-6">
                        <div class="card">
                            <img src="${book.book_image}" class="card-img-top" alt="${translatedTitle}">
                            <div class="card-body">
                                <h5 class="card-title">${translatedTitle}</h5>
                                <p class="card-text">Autor: ${book.author}</p>
                                <p class="card-text">${translatedDesc}</p>
                                <a href="${book.amazon_product_url}" target="_blank" class="btn btn-primary">Comprar en Amazon</a>
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

// 🔹 Llama a la función al cargar la página
document.addEventListener('DOMContentLoaded', fetchNYTBooks);


