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




-- 1:
SELECT *
FROM orders AS o
JOIN order_detail2 AS od
ON o.id = od.order_id
JOIN payments AS p
ON o.id = p.order_id;


SELECT 
YEAR(o.order_date) AS sale_year,
MONTH(o.order_date) AS sale_month,
COUNT(DISTINCT o.id) AS order_count,
SUM(od.quantity) AS total_items,
SUM(p.total_amount) AS total_sales
FROM orders AS o
JOIN order_detail2 AS od
ON o.id = od.order_id
JOIN payments AS p
ON o.id = p.order_id
GROUP BY 
YEAR(o.order_date),
MONTH(o.order_date)
ORDER BY 
sale_year,
sale_month;


-- 2:

SELECT 
u.id,
u.first_name,
u.last_name,
SUM(p.total_amount) AS sum_amount,
AVG(p.total_amount) AS avg_amount
FROM users AS u
JOIN orders AS o
ON u.id = o.user_id
JOIN payments AS p
ON o.id = p.order_id
GROUP BY 
u.id,
u.first_name,
u.last_name
HAVING COUNT(o.id) > 1
ORDER BY sum_amount DESC;



-- 3:

SELECT 
	p.id,
    p.title,
    COUNT(od.order_id) AS number_of_sales,
    SUM(od.quantity) AS sold_qty,
    SUM(od.quantity * od.price) AS revenue
FROM products AS p
JOIN order_detail2 AS od
ON p.id = od.product_id
GROUP BY 
	p.id,
    p.title
ORDER BY revenue DESC
LIMIT 10
;


-- 4:
SELECT 
	c.title,
    COUNT(DISTINCT p.id) AS product_count,
    SUM(od.quantity) AS sold_items,
    SUM(od.quantity * od.price) AS revenue
FROM categories AS c
JOIN products AS p
ON c.id = p.category_id
JOIN order_detail2 AS od
ON p.id = od.product_id
GROUP BY 
	c.id,
    c.title
ORDER BY revenue DESC;


-- 5:
SELECT 
	sales_channel,
    COUNT(o.id) AS num_of_orders,
    COUNT(DISTINCT o.user_id) AS num_of_customers,
    SUM(p.total_amount) AS total_sales,
    AVG(p.total_amount) AS avg_total_sales
FROM orders AS o
JOIN payments AS p
ON p.order_id = o.id
GROUP BY sales_channel;


