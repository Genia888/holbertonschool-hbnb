/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {


    // Ftech detailed place if token and place id identified
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get("id");
    
    try {
      if (placeId) {
        fetchDetailedPlace('', placeId);
      }
      else
      {
        /* DO SOMETHING */
        fetchPlaces('');
      }
    } catch (error) {
      console.error(error);
    }
  });

/** Places fetch and display */
async function fetchPlaces(token) {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {

    });
    /*      headers: {
        Authorization: `Bearer ${token}`,
      },*/
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error("Error fetching places:", error);
  }
}


function displayPlaces(places) {
  const placesList = document.getElementById("places-list");
  placesList.innerHTML = "";
  places.forEach((place) => {
    const placeCard = document.createElement("div");
    placeCard.className = "place-card";
    placeCard.innerHTML = `
      <a href="place.html?id=${place.id}" class="place-card-image">
        ${place.title}
      </a>
      <div class="place-card-content">
        <h2>${place.title}</h2>
        <p class="description">${place.description}</p>
        <p class="price-card"><strong>${place.price} €</strong> per night</p>
      </div>
    `;
    placesList.appendChild(placeCard);
  });
  /*applyPriceFilter();*/
}

/** Place Details Fetch and Display */
async function fetchDetailedPlace(token, placeId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/places/${placeId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (response.ok) {
      const detailedPlace = await response.json();
      displayDetailedPlaces(detailedPlace);
    } else {
      console.error("Failed to fetch detailed place.");
    }
  } catch (error) {
    console.error("Error fetching place detail:", error);
  }
}

function displayDetailedPlaces(place) {
  document.getElementById("place-details").innerHTML = `
        <h1 class="detailedTitle">${place.title}</h1>
        <p class="detailedDescription">${place.description}</p>
        <p class="amenities">What this place offers: 

        </p>
        <div class='addButtonContainer'><a href="add_review.html?id=${
          place.id
        }"><button>Add a review</button></a></div>
    `;

  const reviewsPlace = document.getElementById("reviews");

  if (place.reviews && place.reviews.length > 0) {
    place.reviews.forEach((review) => {
      const reviewCard = document.createElement("div");
      reviewCard.classList.add("review-card");
      reviewCard.innerHTML = `
                <p>${review.text}</p>
                <p><strong>Rating: ${review.rating}/5</strong></p>
            `;
      reviewsPlace.appendChild(reviewCard);
    });
  } else {
    reviewsPlace.innerHTML += "<p>No reviews available for this place.</p>";
  }
  //initializeCarousel();
}