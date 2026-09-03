USE KohanNegar;

SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM users;
SELECT * FROM user_roles;
SELECT * FROM roles;
SELECT * FROM discount;
SELECT * FROM orders;
SELECT * FROM order_detail2;
SELECT * FROM payments;
SELECT * FROM user_basket;




SELECT *
FROM orders AS o
JOIN order_detail2 AS od
ON o.id = od.order_id
JOIN payments AS p
ON o.id = p.order_id;