// setup.php
<?php
$host = 'localhost';
$username = 'root';
$password = '';
$dbname = 'food_billing';

// Create connection
$conn = new mysqli($host, $username, $password);

// Check connection
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error);
}

// Create the database if it doesn't exist
$sql = "CREATE DATABASE IF NOT EXISTS $dbname";
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully or already exists.<br>";
} else {
    die("Error creating database: " . $conn->error);
}

// Use the new database
$conn->select_db($dbname);

// Create the products table if it doesn't exist
$sql = "CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255) NOT NULL
)";

if ($conn->query($sql) === TRUE) {
    echo "Table created successfully or already exists.<br>";
} else {
    die("Error creating table: " . $conn->error);
}

// Delete all existing rows to avoid duplicates
$sql = "TRUNCATE TABLE products";
if ($conn->query($sql) === TRUE) {
    echo "All existing data deleted successfully.<br>";
} else {
    die("Error deleting data: " . $conn->error);
}

// Insert new data with local image paths
$sql = "INSERT INTO products (name, description, price, image_url) VALUES
('Burger', 'Juicy grilled beef patty with fresh vegetables.', 10.00, 'images/Burger.jpg'),
('Pizza', 'Cheese-loaded pizza with toppings of your choice.', 8.00, 'images/Pizza.jpg'),
('Pasta', 'Creamy pasta with mushrooms and chicken.', 7.00, 'images/Pasta.jpg'),
('Sandwich', 'Whole-grain sandwich with egg and avocado.', 6.00, 'images/Sandwich.jpg'),
('Salad', 'Fresh garden salad with vinaigrette dressing.', 5.00, 'images/Salad.jpg'),
('Juice', 'Freshly squeezed orange juice.', 4.00, 'images/Juice.jpg'),
('Ice Cream', 'Delicious vanilla ice cream with toppings.', 3.00, 'images/IceCream.jpg'),
('Coffee', 'Hot brewed coffee with milk or black.', 2.00, 'images/Coffee.jpg')";

if ($conn->query($sql) === TRUE) {
    echo "Sample data inserted successfully.<br>";
} else {
    echo "Error inserting data: " . $conn->error;
}

// Close connection
$conn->close();
?>
