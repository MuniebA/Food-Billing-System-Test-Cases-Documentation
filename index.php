<?php
include 'db.php';

// Fetch all products from the database
$query = "SELECT * FROM products";
$result = $conn->query($query);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Billing System</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="main-container">
        <div class="content-area">
            <div class="header">
                <h1>Food Billing System</h1>
                <p class="subtitle">Select items and quantities to generate bill</p>
            </div>
            
            <div class="food-list">
                <div class="food-items">
                    <?php while ($row = $result->fetch_assoc()): ?>
                        <div class="item" data-price="<?= $row['price']; ?>">
                            <img src="<?= $row['image_url']; ?>" alt="<?= $row['name']; ?>">
                            <div class="item-details">
                                <h2><?= $row['name']; ?></h2>
                                <p class="description"><?= $row['description']; ?></p>
                                <div class="price-quantity">
                                    <span class="price">$<?= number_format($row['price'], 2); ?></span>
                                    <input type="number" min="0" placeholder="Qty" class="quantity">
                                </div>
                            </div>
                        </div>
                    <?php endwhile; ?>
                </div>
            </div>
        </div>

        <div class="sidebar">
            <div class="bill-card">
                <div class="options-section">
                    <h2>Billing Options</h2>
                    <div class="checkbox-wrapper">
                        <label class="discount-toggle" for="discount">
                            <input 
                                type="checkbox" 
                                id="discount" 
                                name="discount"
                                style="width: 20px; height: 20px; margin-right: 10px; cursor: pointer; position: relative; z-index: 10;"
                                data-testid="discount-checkbox"
                            >
                            <span class="toggle-label" style="position: relative; z-index: 1;">Apply 50% Discount</span>
                        </label>
                    </div>
                    <button id="calculate" class="calculate-btn">Calculate Bill</button>
                </div>
                
                <div class="bill-summary">
                    <h2>Bill Summary</h2>
                    <div id="bill-details"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>

<?php
$conn->close();
?>