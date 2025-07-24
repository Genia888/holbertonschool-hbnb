-- ADMIN user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.com',
    '$2b$12$3TW4nUNVtMOSc4LKP5Eeb.Zrw/9oCS6pGRtKIMNabpM9ieOMTy/sq',
    TRUE
);

-- AMENITIES
INSERT INTO amenities (id, name) VALUES
('5f6d9b71-a1cc-4bfc-9c3e-d998a9f994f1', 'WiFi'),
('9e38c654-d490-4fe9-93d5-80f0035185c6', 'Swimming Pool'),
('2bc91d2a-d88c-4a1d-9461-e1ff397dbfe6', 'Garage');

-- USERS (avec toutes les colonnes)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES
('1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', 'Soso', 'Doe', 'soso@example.com', 'Soso12345', FALSE),
('2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', 'MrPhillips', 'Smith', 'doudou@example.com', 'Doudou12345', FALSE),
('3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'Evgen', 'Johnson', 'evgen@example.com', 'Evgen12345', FALSE);

-- PLACES
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES
('4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9', 'Cozy suite in Kiev', 'A cozy cottage in Kiev.', 100.00, 40.7128, -74.0060, '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p'),
('5e6f7g8h-9i0j-1k2l-3m4n-5o6p7q8r90', 'Alger Villa', 'A luxurious villa by the beach in Alger.', 250.00, 34.0522, -118.2437, '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q'),
('6f7g8h9i-0j1k-2l3m-4n5o6p7q8r9-0', 'Villa of Doudou', 'A peaceful retreat in the mountains.', 150.00, 37.7749, -122.4194, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r');

-- PLACE AMENITIES
INSERT INTO place_amenity (place_id, amenity_id)
VALUES
('4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9', '5f6d9b71-a1cc-4bfc-9c3e-d998a9f994f1'), -- WiFi
('5e6f7g8h-9i0j-1k2l-3m4n-5o6p7q8r90', '9e38c654-d490-4fe9-93d5-80f0035185c6'), -- Swimming Pool
('6f7g8h9i-0j1k-2l3m-4n5o6p7q8r9-0', '2bc91d2a-d88c-4a1d-9461-e1ff397dbfe6'); -- Garage

-- REVIEWS
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES
('7g8h9i0j-1k2l-3m4n-5o6p7q8r9-0', 'Great place to Ukraine!', 5, '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', '4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9'),
('8h9i0j1k-2l3m-4n5o6p7q8r9-0', 'Loved the beachfront view!', 4, '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', '5e6f7g8h-9i0j-1k2l-3m4n-5o6p7q8r90'),
('9i0j1k2l-3m-4n5o6p7q8r9-0', 'A perfect villa.', 5, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', '6f7g8h9i-0j1k-2l3m-4n5o6p7q8r9-0');
