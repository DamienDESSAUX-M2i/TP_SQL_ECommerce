INSERT INTO categories(name_category, description_category) VALUES
('Électronique','Produits high-tech et accessoires'),
('Maison & Cuisine','Électroménager et ustensiles'),
('Sport & Loisirs','Articles de sport et plein air'),
('Beauté & Santé','Produits de beauté, hygiène, bien-être'),
('Jeux & Jouets','Jouets pour enfants et adultes');

INSERT INTO products(name_product, price, stock, id_category) VALUES
('Casque Bluetooth X1000',79.99,50,(SELECT id_category FROM categories WHERE name_category='Électronique')),
('Souris Gamer Pro RGB',49.90,120,(SELECT id_category FROM categories WHERE name_category='Électronique')),
('Bouilloire Inox 1.7L',29.99,80,(SELECT id_category FROM categories WHERE name_category='Maison & Cuisine')),
('Aspirateur Cyclonix 3000',129.00,40,(SELECT id_category FROM categories WHERE name_category='Maison & Cuisine')),
('Tapis de Yoga Comfort+',19.99,150,(SELECT id_category FROM categories WHERE name_category='Sport & Loisirs')),
('Haltères 5kg (paire)',24.99,70,(SELECT id_category FROM categories WHERE name_category='Sport & Loisirs')),
('Crème hydratante BioSkin',15.90,200,(SELECT id_category FROM categories WHERE name_category='Beauté & Santé')),
('Gel douche FreshEnergy',4.99,300,(SELECT id_category FROM categories WHERE name_category='Beauté & Santé')),
('Puzzle 1000 pièces "Montagne"',12.99,95,(SELECT id_category FROM categories WHERE name_category='Jeux & Jouets')),
('Jeu de société "Galaxy Quest"',29.90,60,(SELECT id_category FROM categories WHERE name_category='Jeux & Jouets'));

INSERT INTO customers(first_name, last_name, email, registration_ts) VALUES
('Alice','Martin','alice.martin@mail.com','2024-01-10 14:32'),
('Bob','Dupont','bob.dupont@mail.com','2024-02-05 09:10'),
('Chloé','Bernard','chloe.bernard@mail.com','2024-03-12 17:22'),
('David','Robert','david.robert@mail.com','2024-01-29 11:45'),
('Emma','Leroy','emma.leroy@mail.com','2024-03-02 08:55'),
('Félix','Petit','felix.petit@mail.com','2024-02-18 16:40'),
('Hugo','Roussel','hugo.roussel@mail.com','2024-03-20 19:05'),
('Inès','Moreau','ines.moreau@mail.com','2024-01-17 10:15'),
('Julien','Fontaine','julien.fontaine@mail.com','2024-01-23 13:55'),
('Katia','Garnier','katia.garnier@mail.com','2024-03-15 12:00');

INSERT INTO orders(id_customer, order_ts, status_order) VALUES
((SELECT id_customer FROM customers WHERE email='alice.martin@mail.com'),'2024-03-01 10:20','PAID'),
((SELECT id_customer FROM customers WHERE email='bob.dupont@mail.com'),'2024-03-04 09:12','SHIPPED'),
((SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com'),'2024-03-08 15:02','PAID'),
((SELECT id_customer FROM customers WHERE email='david.robert@mail.com'),'2024-03-09 11:45','CANCELLED'),
((SELECT id_customer FROM customers WHERE email='emma.leroy@mail.com'),'2024-03-10 08:10','PAID'),
((SELECT id_customer FROM customers WHERE email='felix.petit@mail.com'),'2024-03-11 13:50','PENDING'),
((SELECT id_customer FROM customers WHERE email='hugo.roussel@mail.com'),'2024-03-15 19:30','SHIPPED'),
((SELECT id_customer FROM customers WHERE email='ines.moreau@mail.com'),'2024-03-16 10:00','PAID'),
((SELECT id_customer FROM customers WHERE email='julien.fontaine@mail.com'),'2024-03-18 14:22','PAID'),
((SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com'),'2024-03-20 18:00','PENDING');

INSERT INTO order_items(id_order, id_product, quantity, price) VALUES
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='alice.martin@mail.com') AND order_ts='2024-03-01 10:20'),(SELECT id_product FROM products WHERE name_product='Casque Bluetooth X1000' LIMIT 1),1,79.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='alice.martin@mail.com') AND order_ts='2024-03-01 10:20'),(SELECT id_product FROM products WHERE name_product='Puzzle 1000 pièces "Montagne"' LIMIT 1),2,12.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='bob.dupont@mail.com') AND order_ts='2024-03-04 09:12'),(SELECT id_product FROM products WHERE name_product='Tapis de Yoga Comfort+' LIMIT 1),1,19.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com') AND order_ts='2024-03-08 15:02'),(SELECT id_product FROM products WHERE name_product='Bouilloire Inox 1.7L' LIMIT 1),1,29.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='chloe.bernard@mail.com') AND order_ts='2024-03-08 15:02'),(SELECT id_product FROM products WHERE name_product='Gel douche FreshEnergy' LIMIT 1),3,4.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='david.robert@mail.com') AND order_ts='2024-03-09 11:45'),(SELECT id_product FROM products WHERE name_product='Haltères 5kg (paire)' LIMIT 1),1,24.99),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='emma.leroy@mail.com') AND order_ts='2024-03-10 08:10'),(SELECT id_product FROM products WHERE name_product='Crème hydratante BioSkin' LIMIT 1),2,15.90),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='julien.fontaine@mail.com') AND order_ts='2024-03-18 14:22'),(SELECT id_product FROM products WHERE name_product='Jeu de société "Galaxy Quest"' LIMIT 1),1,29.90),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com') AND order_ts='2024-03-20 18:00'),(SELECT id_product FROM products WHERE name_product='Souris Gamer Pro RGB' LIMIT 1),1,49.90),
((SELECT id_order FROM orders WHERE id_customer=(SELECT id_customer FROM customers WHERE email='katia.garnier@mail.com') AND order_ts='2024-03-20 18:00'),(SELECT id_product FROM products WHERE name_product='Gel douche FreshEnergy' LIMIT 1),2,4.99);