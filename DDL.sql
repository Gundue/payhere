CREATE DATABASE cafe DEFAULT CHARACTER SET utf8mb4;

-- USER TABLE
CREATE TABLE cafe.user (
  id int(11) NOT NULL AUTO_INCREMENT,
  phone varchar(11),
  password varchar(128),
  name varchar(10),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TOKEN TABLE
CREATE TABLE cafe.token (
  user_id int(11) NOT NULL AUTO_INCREMENT,
  access_token varchar(255) NOT NULL,
  created_at datetime DEFAULT NULL,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PRODUCT TABLE
CREATE TABLE cafe.product (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  category varchar(50),
  price varchar(10),
  cost varchar(10),
  name varchar(50),
  description varchar(100),
  barcode varchar(20),
  expiration_date datetime,
  size enum('small','large'),
  PRIMARY KEY (id),
  KEY user_id (user_id),
  CONSTRAINT product_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;