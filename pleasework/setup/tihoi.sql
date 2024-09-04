-- code to enable referential integrity
PRAGMA foreign_keys = 1;


DROP TABLE IF EXISTS tbl_purchs_items;
DROP TABLE IF EXISTS tbl_purchs;
DROP TABLE IF EXISTS tbl_filters;
drop table if exists tbl_filters_names;
DROP TABLE IF EXISTS tbl_items;
--delete the tables if they already exist so that I can easily edit entities.

CREATE TABLE tbl_items(
  	id INT,
	name VARCHAR(50),
  	cost FLOAT,
  	image BLOB,
  	stock INT,
    PRIMARY KEY (id)
);

INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(1,'Tramping Bag',200,'img',20);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(2,'Pack Liner',15,'img',70);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(3,'Sleeping Bag',125,'img',30);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(4,'Roll Mat',40,'img',25);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(5,'Rain Jacket',100,'img',80);


CREATE table tbl_filters_names(
  id INT,
  name varchar(50),
  primary key(id)
);
insert into tbl_filters_names (id, name) values(1, 'Essential');
insert into tbl_filters_names (id, name) values(2, 'Popular');
insert into tbl_filters_names (id, name) values(3, 'Clothing');


CREATE TABLE tbl_filters(
	id INT,
  	name_id INT,
    PRIMARY KEY(id, name_id),
  	FOREIGN KEY(id) REFERENCES tbl_items(id),
  	FOREIGN Key(name_id) references tbl_filters_names(id)
);
INSERT INTO tbl_filters (id, name_id) VALUES(1,1);
INSERT INTO tbl_filters (id, name_id) VALUES(1,2);
INSERT INTO tbl_filters (id, name_id) VALUES(2,1);
INSERT INTO tbl_filters (id, name_id) VALUES(3,1);
INSERT INTO tbl_filters (id, name_id) VALUES(3,2);
INSERT INTO tbl_filters (id, name_id) VALUES(4,1);
INSERT INTO tbl_filters (id, name_id) VALUES(5,1);
INSERT INTO tbl_filters (id, name_id) VALUES(5,3);
INSERT INTO tbl_filters (id, name_id) VALUES(5,2);


CREATE TABLE tbl_purchs(
    id INT,
    total FLOAT,
    sale_date DATETIME,
  	email VARCHAR(200),
    PRIMARY KEY(id)
);

INSERT INTO tbl_purchs (id, total, sale_date, email) VALUES(1,0,'2024-04-03 18:41:15', 'o.walsdorf@stpauls.school.nz');
INSERT INTO tbl_purchs (id, total, sale_date, email) VALUES(2,0,'2024-04-03 19:21:31', 'j.su2@stpauls.school.nz');
INSERT INTO tbl_purchs (id, total, sale_date, email) VALUES(3,0,'2024-04-03 13:12:08', 'l.cao@stpauls.school.nz');


CREATE TABLE tbl_purchs_items(
    purchase_id INT,
    item_id INT,
    quantity INT,
    PRIMARY KEY(purchase_id, item_id),
    FOREIGN KEY(purchase_id) REFERENCES tbl_purchs(id),
    FOREIGN KEY(item_id) REFERENCES tbl_items(id)
);

INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,1,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,2,2);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,3,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(2,4,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,5,2);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,1,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,2,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,3,1);

