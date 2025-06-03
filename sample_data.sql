-- Insert dummy users
INSERT INTO users (email, password_hash, first_name, last_name)
VALUES ('john@example.com', 'dummyhash123', 'John', 'Doe');

-- Insert dummy doctors
INSERT INTO doctors (first_name, last_name, short_bio, gender, specialty, languages, rating, profile_image, city)
VALUES
('John', 'Doe', 'Experienced general dentist', 'M', 'General Dentistry', 'English,Hindi', 4.5, 'doctor1.png', 'Mumbai'),
('Sarah', 'Lee', 'Pediatric dental specialist', 'F', 'Pediatric Dentistry', 'English', 4.8, 'doctor2.png', 'Delhi');

-- Insert dummy products
INSERT INTO products (name, description, image_url, price, category)
VALUES
('Electric Toothbrush', 'Rechargeable with pressure sensor', 'toothbrush.png', 2499.99, 'Oral Care'),
('Whitening Strips', 'For brighter teeth in 7 days', 'whitening.png', 799.00, 'Whitening');
