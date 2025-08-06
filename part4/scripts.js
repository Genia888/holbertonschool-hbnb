// Helper pour lire un cookie par son nom
function getCookie(name) {
  const cookieStr = document.cookie.split('; ').find(row => row.startsWith(name + '='));
  return cookieStr ? decodeURIComponent(cookieStr.split('=')[1]) : null;
}

// 🔧 Supprimer un cookie
function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/`;
}

// Vérifie et affiche l'utilisateur connecté
async function checkUserAuthentication() {
  const token = getCookie('token');
  const userDisplay = document.getElementById('user-info');
  const logoutBtn = document.getElementById('logout-button');
  const loginBtn = document.querySelector('.login-button');

  if (!token) {
    if (loginBtn) loginBtn.style.display = 'inline';
    if (userDisplay) userDisplay.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'none';
    return;
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/v1/auth/me', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.ok) {
      const user = await res.json();
      if (userDisplay) {
        userDisplay.textContent = `Welcome, ${user.first_name}`;
        userDisplay.style.display = 'inline';
      }
      if (logoutBtn) logoutBtn.style.display = 'inline';
      if (loginBtn) loginBtn.style.display = 'none';
    } else {
      deleteCookie('token');
      if (!window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
      }
    }
  } catch (err) {
    console.error('Auth check failed:', err);
    deleteCookie('token');
    if (!window.location.pathname.includes('login.html')) {
      window.location.href = 'login.html';
    }
  }
}

function setupLogoutListener() {
  const logoutBtn = document.getElementById('logout-button');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      deleteCookie('token');
      window.location.href = 'login.html';
    });
  }
}

function setupLoginForm() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorMessage = document.getElementById('error-message');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
      } else {
        errorMessage.textContent = data.error || 'Login failed.';
      }
    } catch (err) {
      console.error('Login error:', err);
      errorMessage.textContent = 'Connection failed.';
    }
  });
}

function loadPlacesIfOnIndex() {
  if (!window.location.pathname.includes('index.html') && window.location.pathname !== '/') return;

  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  if (!placesList) return;

  fetch('http://127.0.0.1:5000/api/v1/places/')
    .then(res => res.json())
    .then(data => {
      placesList.innerHTML = '';
      const prices = new Set();
      const images = [
        'images/big house.jpg',
        'images/myhouse.jpg',
        'images/little house.jpg',
        'images/seb.jpg',
        'images/room.jpg',
        'images/hotel morocco.jpg',
        'images/little house.jpg',
        'images/camping.jpg',
        'images/room rodez.jpg',
        'images/castle.jpg',
        'images/kiev.jpg',
        'images/house.jpg',
      ];

      data.forEach((place, idx) => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
          <img src="${place.image_url || images[idx % images.length]}" alt="Photo de ${place.title}" class="place-photo">
          <h3>${place.title}</h3>
          <p><strong>Price:</strong> ${place.price}€ / night</p>
          <button class="details-button" data-id="${place.id}">View Details</button>
        `;
        card.querySelector('.details-button').addEventListener('click', () => {
          window.location.href = `place.html?id=${place.id}`;
        });
        placesList.appendChild(card);
        prices.add(Math.ceil(place.price));
      });

      /*[...prices].sort((a, b) => a - b).forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = `≤ ${price}€`;
        priceFilter.appendChild(option);
      });*/

      priceFilter.addEventListener('change', () => {
        const max = parseFloat(priceFilter.value);
        Array.from(placesList.children).forEach(card => {
          const priceText = card.querySelector('p').textContent;
          const match = priceText.match(/(\d+(\.\d+)?)/);
          const price = match ? parseFloat(match[0]) : 0;
          // Si le filtre est vide ou non numérique, afficher toutes les places
          if (!priceFilter.value || isNaN(max)) {
            card.style.display = 'block';
          } else {
            card.style.display = price <= max ? 'block' : 'none';
          }
        });
      });
    })
    .catch(err => {
      console.error('Failed to fetch places:', err);
      placesList.innerHTML = `<p class="error">Failed to load places.</p>`;
    });
}

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

function fetchPlaceDetails(placeId, token = null) {
  const placeDetailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');

  // Récupère toutes les places pour retrouver l'index
  fetch('http://127.0.0.1:5000/api/v1/places/')
    .then(res => res.json())
    .then(allPlaces => {
      // Trouve l'index de la place courante
      const idx = allPlaces.findIndex(p => String(p.id) === String(placeId));
      const defaultImages = [
        'images/big house.jpg',
        'images/myhouse.jpg',
        'images/little house.jpg',
        'images/seb.jpg',
        'images/room.jpg',
        'images/hotel morocco.jpg',
        'images/little house.jpg',
        'images/camping.jpg',
        'images/room rodez.jpg',
        'images/castle.jpg',
        'images/kiev.jpg',
        'images/house.jpg',
      ];
      fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
        .then(response => response.json())
        .then(place => {
          let amenitiesHtml = '';
          if (place.amenities && place.amenities.length > 0) {
            amenitiesHtml = `<p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>`;
          }
          // Utilise l'image_url si présente, sinon la même image que sur l'index
          let imageHtml = '';
          if (place.image_url) {
            imageHtml = `<img src="${place.image_url}" alt="Photo de ${place.title}" class="place-photo">`;
          } else {
            const imgSrc = defaultImages[idx >= 0 ? idx % defaultImages.length : 0];
            imageHtml = `<img src="${imgSrc}" alt="Photo de ${place.title}" class="place-photo">`;
          }
          placeDetailsSection.innerHTML = `
            <div class="place-info">
              ${imageHtml}
              <h2>${place.title}</h2>
              <p>${place.description}</p>
              <p><strong>Price:</strong> ${place.price}€</p>
              <p><strong>Latitude:</strong> ${place.latitude}</p>
              <p><strong>Longitude:</strong> ${place.longitude}</p>
              ${amenitiesHtml}
            </div>
          `;
        });
    });

  fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`)
    .then(response => response.json())
    .then(reviews => {
      if (reviews.length === 0) {
        reviewsSection.innerHTML = "<p>No reviews yet.</p>";
      } else {
        reviews.forEach(review => {
          const reviewCard = document.createElement('div');
          reviewCard.className = 'review-card';
          // Affiche le nom de l'utilisateur si disponible
          const userName = review.user_first_name || review.user_name || 'Utilisateur';
          reviewCard.innerHTML = `
            <div class="review-header">
              <span class="review-avatar">${userName.charAt(0).toUpperCase()}</span>
              <span class="review-user"><strong>${userName}</strong></span>
              <span class="review-sep">|</span>
              <span class="review-action">rated</span>
              <span class="review-rating"><strong>${review.rating}/5</strong> <span class="star">★</span></span>
            </div>
            <div class="review-body">${review.text}</div>
          `;
          reviewsSection.appendChild(reviewCard);
        });
      }

      // Affichage dynamique du formulaire d'ajout de review
      const addReviewSection = document.getElementById('add-review');
      const token = getCookie('token');
      if (!addReviewSection) return;
      if (!token) {
        addReviewSection.classList.remove('active');
        return;
      }
      // Récupère l'utilisateur connecté
      fetch('http://127.0.0.1:5000/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(user => {
          // Vérifie si user est propriétaire ou a déjà review
          const isOwner = reviews.length > 0 && reviews.some(r => r.user_id === user.id && r.user_first_name === user.first_name);
          const hasReviewed = reviews.some(r => r.user_id === user.id);
          if (isOwner || hasReviewed) {
            addReviewSection.classList.remove('active');
          } else {
            addReviewSection.classList.add('active');
          }
        })
        .catch(() => addReviewSection.classList.remove('active'));
    });
}

function setupReviewForm() {
  const reviewForm = document.getElementById('review-form');
  const placeId = getPlaceIdFromURL();
  const token = getCookie('token');

  if (reviewForm && placeId && token) {
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const reviewText = document.getElementById('review-text').value.trim();
      const rating = document.querySelector('input[name="rating"]:checked')?.value;
      const error = document.getElementById('review-error');
      const success = document.getElementById('review-success');

      if (!rating) {
        error.textContent = 'Please select a rating.';
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
        });

        if (response.ok) {
          success.textContent = 'Review submitted successfully!';
          reviewForm.reset();
          error.textContent = '';
        } else {
          const data = await response.json();
          error.textContent = data.error || 'Failed to submit review.';
          success.textContent = '';
        }
      } catch (err) {
        console.error('Review submission error:', err);
        error.textContent = 'Something went wrong. Please try again.';
        success.textContent = '';
      }
    });
  }
}


document.addEventListener('DOMContentLoaded', () => {
  checkUserAuthentication();
  setupLogoutListener();
  setupLoginForm();
  loadPlacesIfOnIndex();
  setupReviewForm();
  if (window.location.pathname.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(placeId);
  }
});

// Ajout de sécurité : ne rien faire si le bouton login n'existe pas (pour compatibilité toutes pages)
document.addEventListener('DOMContentLoaded', () => {
  const loginLink = document.getElementById('login-link');
  // Si c'est un <button> (rare), on ajoute un handler, sinon rien à faire pour un <a>
  if (loginLink && loginLink.tagName === 'BUTTON') {
    loginLink.onclick = function() {
      window.location.href = 'login.html';
    };
  }
});