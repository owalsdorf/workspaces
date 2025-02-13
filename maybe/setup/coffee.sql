DROP table if exists tbl_items;

CREATE TABLE tbl_items(
  id    VARCHAR(50) PRIMARY KEY,
  sku   VARCHAR(50),
  name  VARCHAR(50),
  cat   VARCHAR(50),
  size  VARCHAR(50),
  price INT
);
INSERT INTO tbl_items(id,sku,name,cat,size,price) VALUES 
('It001','HDR-CAP-MD','Cappuccino','Hot Drinks','Medium',3.45),
('It002','HDR-CAP-LG','Cappuccino','Hot Drinks','Large',3.75),
('It003','HDR-LAT-MD','Latte','Hot Drinks','Medium',3.45),
('It004','HDR-LAT-LG','Latte','Hot Drinks','Large',3.75),
('It005','HDR-FLT','Flat White','Hot Drinks','N/A',3.15),
('It006','HDR-CRM-MD','Caramel Macchiato','Hot Drinks','Medium',4.20),
('It007','HDR-CRM-LG','Caramel Macchiato','Hot Drinks','Large',4.60),
('It008','HDR-ESP','Espresso','Hot Drinks','N/A',2.15),
('It009','HDR-MOC-MD','Mocha','Hot Drinks','Medium',4.00),
('It010','HDR-MOC-LG','Mocha','Hot Drinks','Large',4.60),
('It011','HDR-WMO-MD','White Mocha','Hot Drinks','Medium',4.50),
('It012','HDR-WMO-LG','White Mocha','Hot Drinks','Large',4.70),
('It013','HDR-HCH-MD','Hot Chocolate','Hot Drinks','Medium',4.20),
('It014','HDR-HCH-LG','Hot Chocolate','Hot Drinks','Large',4.60),
('It015','CDR-CCF-MD','Cold Coffee','Cold Drinks','Medium',3.45),
('It016','CDR-CCF-LG','Cold Coffee','Cold Drinks','Large',3.75),
('It017','CDR-CMO-MD','Cold Mocha','Cold Drinks','Medium',4.00),
('It018','CDR-CMO-LG','Cold Mocha','Cold Drinks','Large',4.60),
('It019','CDR-ICT-MD','Iced Tea','Cold Drinks','Medium',3.25),
('It020','CDR-ICT-LG','Iced Tea','Cold Drinks','Large',3.55),
('It021','CDR-LMN-MD','Lemonade','Cold Drinks','Medium',3.35),
('It022','CDR-LMN-LG','Lemonade','Cold Drinks','Large',3.75),
('It023','SNK-SHC','Sandwich Ham&Cheese','Snacks','N/A',5.60),
('It024','SNK-SSM','Sandwich Salami&Mozzarella','Snacks','N/A',5.50)
