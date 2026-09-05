USE market;
SET @new_created_user_id = UUID();


insert into users (user_id, username, password, first_name, last_name, birth_date)
VALUES (@new_created_user_id , 'Mmm114', 'vjfvjtrv kvmnrcs', 'mohammad', 'mostavai', '2000-11-10');




SELECT * FROM roles;

INSERT INTO user_roles (role_id, user_id) 
VALUES (1, @new_created_user_id);

INSERT INTO user_roles (role_id, user_id) 
VALUES (2, @new_created_user_id);


INSERT INTO user_roles (role_id, user_id) 
VALUES (3, @new_created_user_id);


SELECT * FROM users;
SELECT * FROM user_roles;


INSERT INTO categories (title, parent_id)
VALUES 
	('supermarket', null) ,
	('electric', null) ,
	('cloths', null),
	('toys', null);

SELECT * FROM categories;


SHOW CREATE TABLE products;
SHOW CREATE TABLE categories;

INSERT INTO categories (title, parent_id)
VALUES 
	('milk', 1) ,
	('meat', 1) ,
	('pasta', 1),
	('air fryer', 2),
    ('refrigator', 2),
    ('fan', 2),
    ('lamp', 2),
    ('t-shirt', 3),
    ('doll',4)
;

SELECT * FROM categories;


INSERT INTO products (title, detail, price, category_id) 
VALUES 
	('condensed milk', null, 150000, 5),
	('choclate milk', null, 200000, 5),
	('navy t-shirt', null, 530000, 12)
;

SELECT * FROM products;

INSERT INTO user_basket (user_id, product_id, quantity) 
VALUES
	('b863a49a-a90d-11f1-83a3-24d6c7608b97',16, 3);



INSERT INTO orders (user_id, order_date) VALUES
('b863a49a-a90d-11f1-83a3-24d6c7608b97', CURRENT_TIMESTAMP());

INSERT INTO order_detail (order_id, product_id, quantity, price)
SELECT 1, ub.product_id, ub.quantity, p.price
FROM user_basket AS ub
INNER JOIN products AS p
ON p.idproducts = ub.product_id ;

SELECT * FROM order_detail ;

INSERT INTO order_detail2
    (order_id, detail_id, product_id, quantity, price)
SELECT
    1 AS order_id,
    ROW_NUMBER() OVER (ORDER BY ub.product_id) AS row_id,
    ub.product_id,
    ub.quantity,
    p.price
FROM user_basket AS ub
INNER JOIN products AS p
    ON p.idproducts = ub.product_id;
    
    
SELECT * FROM order_detail2 ;
SELECT * FROM user_basket;
SET @userid = 'b863a49a-a90d-11f1-83a3-24d6c7608b97';

INSERT INTO orders (user_id) 
VALUES (@userid);

SELECT last_insert_id();
SET @orderid = last_insert_id();

INSERT INTO order_detail2
    (order_id, detail_id, product_id, quantity, price)
SELECT
    @orderid AS order_id,
    ROW_NUMBER() OVER (ORDER BY ub.product_id) AS detail_id,
    ub.product_id,
    ub.quantity,
    p.price
FROM user_basket AS ub
INNER JOIN products AS p
    ON p.idproducts = ub.product_id
WHERE ub.user_id = @userid ;
    
    
DELETE FROM user_basket WHERE user_id = @userid AND product_id > 0;

INSERT INTO discount (title, discount_code, active_date,expired_date, percent)
VALUE ('d1', LEFT(UUID(),8), '2026-09-05', '2026-10-05',10);

SELECT LEFT(UUID(),8);

SELECT * FROM discount;





SELECT 
	id,
    percent
    INTO 
		@id,
        @percent
FROM discount
WHERE discount_code = 'd9c6319c' 
AND
	active_date <= date(now())
AND 
	expired_date >= date(now());
    

SELECT @id, @percent;

SELECT * FROM order_detail;

INSERT INTO payments (order_id, discount_id, total_price, disount_price, total_amount, payment_type, payment_date, 
payment_time, payment_code) 
SELECT 1,@id, price, price * @percent / 100, price - (price * @percent / 100) , 1, date(now()), time(now()), '304748374883'
FROM (
	SELECT SUM(price * quantity) AS price FROM order_detail
	GROUP BY order_id) AS orderdetail
;

-- STORE PROCEEDURE

CALL insert_payment(1, 'd9c6319c' );
DESCRIBE discount;

