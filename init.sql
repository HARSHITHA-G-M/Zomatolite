CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  password VARCHAR(100)
);

CREATE TABLE restaurants (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE menu (
  id INT AUTO_INCREMENT PRIMARY KEY,
  restaurant_id INT,
  item_name VARCHAR(100),
  price DECIMAL(10,2),
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  menu_id INT,
  FOREIGN KEY (menu_id) REFERENCES menu(id)
);

INSERT INTO restaurants (name) VALUES ('Pizza Palace'), ('Burger Bros');

INSERT INTO menu (restaurant_id, item_name, price) VALUES 
(1, 'Pepperoni Pizza', 9.99),
(1, 'Veggie Pizza', 8.49),
(2, 'Cheeseburger', 5.99),
(2, 'Burger', 6.49);

