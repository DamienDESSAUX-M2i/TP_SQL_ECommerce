CREATE TABLE IF NOT EXISTS categories(
   id_categorie uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   name_categorie VARCHAR(255) NOT NULL UNIQUE,
   description_categorie TEXT
);

CREATE TABLE IF NOT EXISTS products(
   id_product uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   name_product VARCHAR(255) NOT NULL,
   price DECIMAL(10,2),
   CONSTRAINT price_strictly_positive CHECK (price > 0),
   stock INT,
   CONSTRAINT stock_positive CHECK (stock >= 0),
   id_categorie uuid NOT NULL,
   CONSTRAINT fk_id_categorie FOREIGN KEY(id_categorie) REFERENCES categories(id_categorie)
);

CREATE TABLE IF NOT EXISTS clients(
   id_client uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   first_name VARCHAR(255) NOT NULL,
   last_name VARCHAR(255) NOT NULL,
   email VARCHAR(255) NOT NULL UNIQUE,
   registration_ts TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS orders(
   id_order uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   order_ts TIMESTAMP NOT NULL,
   status_order VARCHAR(255) NOT NULL,
   CONSTRAINT status_order_enum CHECK (status_order in ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED')),
   id_client uuid NOT NULL,
   CONSTRAINT fk_id_client FOREIGN KEY(id_client) REFERENCES clients(id_client)
);

CREATE TABLE IF NOT EXISTS order_items(
   id_order_item uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   id_product uuid,
   CONSTRAINT kf_id_product FOREIGN KEY(id_product) REFERENCES products(id_product),
   id_order uuid,
   CONSTRAINT kf_id_order FOREIGN KEY(id_order) REFERENCES orders(id_order),
   quantity INT NOT NULL,
   CONSTRAINT quantity_strictly_positive CHECK (quantity > 0),
   price DECIMAL(10,2),
   CONSTRAINT price_strictly_positive CHECK (price > 0)
);
