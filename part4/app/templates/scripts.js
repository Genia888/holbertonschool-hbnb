document.addEventListener('DOMContentLoaded', () => {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  // Fonction pour créer une carte de place
  function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';

    card.innerHTML = `
      <h3>${place.title}</h3>
      <p><strong>Price:</strong> ${place.price}€ / night</p>
      <button class="details-button" data-id="${place.id}">View Details</button>
    `;

    // Ajout de l'événement sur le bouton
    card.querySelector('.details-button').addEventListener('click', () => {
      window.location.href = `place.html?id=${place.id}`;
    });

    return card;
  }

  // Charger les places depuis l’API
  fetch('http://127.0.0.1:5000/api/v1/places/')
    .then(response => response.json())
    .then(data => {
      placesList.innerHTML = '';
      const prices = new Set();

      data.forEach(place => {
        const card = createPlaceCard(place);
        placesList.appendChild(card);
        prices.add(Math.ceil(place.price));
      });

      // Créer les options du filtre prix
      [...prices].sort((a, b) => a - b).forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = `≤ ${price}€`;
        priceFilter.appendChild(option);
      });

      // Filtrage par prix
      priceFilter.addEventListener('change', () => {
        const max = parseFloat(priceFilter.value);
        Array.from(placesList.children).forEach(card => {
          const priceText = card.querySelector('p').textContent;
          const match = priceText.match(/(\d+(\.\d+)?)/);
          const price = match ? parseFloat(match[0]) : 0;
          card.style.display = price <= max ? 'block' : 'none';
        });
      });
    })
    .catch(error => {
      console.error('Failed to fetch places:', error);
      placesList.innerHTML = `<p class="error">Failed to load places.</p>`;
    });
});