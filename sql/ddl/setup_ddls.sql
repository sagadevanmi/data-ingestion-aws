DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price FLOAT NOT NULL,
    stock_available INT NOT NULL
);

-- Create the transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL REFERENCES products(product_id),
    Quantity INT NOT NULL,
    transaction_date DATE NULL,
    total_amount FLOAT NULL
);
