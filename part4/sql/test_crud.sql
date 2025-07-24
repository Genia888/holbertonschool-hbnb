SELECT * FROM users WHERE email = 'admin@hbnb.com';

UPDATE users
SET first_name = 'Evgeny'
WHERE email = 'evgen@example.com';

SELECT * FROM users WHERE email = 'evgen@example.com';

DELETE FROM users WHERE email = 'doudou@example.com';

SELECT * FROM users;

SELECT * FROM amenities;

UPDATE amenities
SET name = 'Private Garage'
WHERE name = 'Garage';

SELECT * FROM amenities WHERE name LIKE '%Garage%';

DELETE FROM amenities WHERE name = 'Swimming Pool';

SELECT * FROM amenities;

SELECT * FROM places WHERE title = 'Alger Villa';

UPDATE places
SET price = 120.00
WHERE title = 'Cozy suite in Kiev';

SELECT * FROM places WHERE title = 'Cozy suite in Kiev';

DELETE FROM places WHERE title = 'Villa of Doudou';

SELECT * FROM places;

SELECT * FROM reviews;

UPDATE reviews
SET text = 'Great place in Ukraine!!!', rating = 4
WHERE user_id = '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p'
  AND place_id = '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9';

SELECT * FROM reviews WHERE place_id = '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9';

DELETE FROM reviews
WHERE user_id = '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q'
  AND place_id = '5e6f7g8h-9i0j-1k2l-3m4n-5o6p7q8r90';

SELECT * FROM reviews;

SELECT * FROM place_amenity
WHERE place_id = '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9';

DELETE FROM place_amenity
WHERE place_id = '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9'
  AND amenity_id = '5f6d9b71-a1cc-4bfc-9c3e-d998a9f994f1';

SELECT * FROM place_amenity WHERE place_id = '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9';
