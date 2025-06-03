CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(2),
    date_of_birth DATETIME,
    avatar_url VARCHAR(255),
    under_physician_care BOOLEAN,
    chronic_conditions BOOLEAN,
    any_allergies BOOLEAN,
    under_medications BOOLEAN,
    pregnant_or_nursing BOOLEAN,
    symptoms JSON,
    previous_treatments JSON,
    diagnosed_gum_disease BOOLEAN,
    brushing_frequency ENUM('Once daily', 'Twice daily', 'Occasionally', 'Rarely'),
    flossing BOOLEAN,
    tobacco_use BOOLEAN,
    sugary_diet BOOLEAN,
    teeth_grinding BOOLEAN,
    is_subscribed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    short_bio TEXT,
    gender VARCHAR(2),
    specialty VARCHAR(250),
    languages VARCHAR(100),
    rating FLOAT,
    profile_image VARCHAR(255),
    city VARCHAR(100)
);

CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    doctor_id INT,
    appointment_time DATETIME,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled'),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    description TEXT,
    image_url VARCHAR(255),
    price DECIMAL(10, 2),
    category VARCHAR(50)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    total_price DECIMAL(10, 2),
    status ENUM('pending', 'paid', 'shipped', 'delivered'),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE scans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    image_url VARCHAR(255),
    oral_health_score INT,
    ai_feedback TEXT,
    detected_conditions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
