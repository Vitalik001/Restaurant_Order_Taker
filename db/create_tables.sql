-- add stats table
-- add column for number of orders of the menu item
CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

COPY menu(name, type, price)
FROM '/code/db/menu.csv'
WITH (FORMAT csv, HEADER true);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    number_of_all_items INT NOT NULL DEFAULT 0
);

CREATE TABLE order_items (
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    number_of_items INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu(id)
);

-- Create a function to calculate and update total_price and number_of_items for an order
CREATE OR REPLACE FUNCTION update_order()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders o
    SET
        total_price = COALESCE((
            SELECT SUM(m.price * oi.number_of_items)
            FROM order_items oi
            JOIN menu m ON oi.menu_item_id = m.id
            WHERE oi.order_id = o.id
        ), 0.00),
        number_of_all_items = COALESCE((
            SELECT SUM(oi.number_of_items)
            FROM order_items oi
            WHERE oi.order_id = o.id
        ), 0)
    WHERE o.id = NEW.order_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to automatically update total_price and number_of_items when inserting or updating order_items
CREATE TRIGGER update_order_trigger
AFTER INSERT OR UPDATE ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_order();
