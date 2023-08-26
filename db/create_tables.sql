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
    total_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE order_items (
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu(id)
);

