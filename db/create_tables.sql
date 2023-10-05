CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    number_of_orders INT NOT NULL DEFAULT 0,
    in_stock INT NOT NULL
);

COPY menu(name, type, price, in_stock)
FROM '/code/db/menu.csv'
WITH (FORMAT csv, HEADER true);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status INT NOT NULL DEFAULT 1
);

CREATE TABLE order_items (
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    number_of_items INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu(id),
    UNIQUE (order_id, menu_item_id)
);

CREATE TABLE chats (
    order_id INT NOT NULL,
    message_id SERIAL,
    message VARCHAR(128) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

CREATE TABLE upsell_stats (
    upsell_id INT NOT NULL,
    asked INT NOT NULL DEFAULT 0,
    accepted INT NOT NULL DEFAULT 0,
    rejected INT NOT NULL DEFAULT 0,
    total_revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (upsell_id) REFERENCES menu(id) ON DELETE CASCADE,
    UNIQUE (upsell_id)

);


-- Create a function to calculate and update total_price for an order
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
        ), 0.00)
    WHERE o.id = NEW.order_id;

    UPDATE menu m
    SET
        number_of_orders = COALESCE((
            SELECT SUM(oi.number_of_items)
            FROM order_items oi
            WHERE oi.menu_item_id = NEW.menu_item_id
        ), 0)
    WHERE m.id = NEW.menu_item_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_total_revenue()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate total_revenue based on accepted and menu price
    SELECT INTO NEW.total_revenue (NEW.accepted * m.price)
    FROM menu m
    WHERE m.id = NEW.upsell_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create a trigger to automatically update total_price when inserting or updating order_items
CREATE TRIGGER update_order_trigger
AFTER INSERT OR UPDATE OR DELETE ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_order();

CREATE TRIGGER update_total_revenue_trigger
BEFORE INSERT OR UPDATE ON upsell_stats
FOR EACH ROW
EXECUTE FUNCTION update_total_revenue();