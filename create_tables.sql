CREATE TABLE user (
    uid INTEGER(5) NOT NULL,
    username VARCHAR(30) NOT NULL,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR(30) NOT NULL,
    email VARCHAR(30),
    password VARCHAR(15) NOT NULL,
    phone VARCHAR(15),
    PRIMARY KEY (uid)
);

CREATE TABLE category (
    cid INTEGER(5) NOT NULL,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (cid)
);

CREATE TABLE medicine (
    mid INTEGER(5) NOT NULL,
    category INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,
    manufacturer VARCHAR(30),
    status VARCHAR(30) NOT NULL,
    demand BIT,
    PRIMARY KEY (mid),
    FOREIGN KEY (category) REFERENCES category (cid)
);

CREATE TABLE `order` (
    oid INTEGER(5) NOT NULL,
    userId INTEGER NOT NULL,
    quantity INTEGER(10) NOT NULL,
    shipDate DATETIME(6),
    status VARCHAR(30) NOT NULL,
    complete BIT,
    PRIMARY KEY (oid),
    FOREIGN KEY (userId) REFERENCES user (uid)
);

CREATE TABLE orders_medicine (
    order_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    PRIMARY KEY (order_id, medicine_id),
    FOREIGN KEY (order_id) REFERENCES `order` (oid),
    FOREIGN KEY (medicine_id) REFERENCES medicine (mid)
    )