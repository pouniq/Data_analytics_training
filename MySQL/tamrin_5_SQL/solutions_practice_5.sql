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

-- 6:
SELECT 

	u.city,
	COUNT(o.id) AS num_of_orders,
	COUNT(DISTINCT o.user_id) AS num_of_customers,
    SUM(p.total_amount) AS total_sales,
    AVG(p.total_amount) AS avg_total_sales
    
FROM users AS u
JOIN orders AS o
ON o.user_id = u.id
JOIN payments AS p
ON p.order_id = o.id
GROUP BY u.city
ORDER BY total_sales DESC;


-- 7: 
SELECT 
	CASE
    WHEN discount_id IS NULL
    THEN 'without discout'
    ELSE 'with discount'
    END AS discount_status,
    
    COUNT(id) AS transaction,
    SUM(total_price) AS before_discount,
    SUM(discount_price) AS discount_amount,
    SUM(total_amount) AS final_sales
    
FROM payments
GROUP BY discount_status;


-- 8:
/*
- investigate the city they are in mostly.
- if they are abled or disabled in the system.
- How old they are ?
- how many days is past after they have registered?
*/

SELECT 
	u.id,
	u.first_name,
	u.last_name,
	u.city, 
    COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o
ON u.id = o.user_id
GROUP BY 
	u.id,
	u.first_name,
	u.last_name,
	u.city
HAVING COUNT(o.id)<=1;


-- 9:


SELECT u.id,
	COUNT(o.id) AS order_count ,
	SUM(p.total_amount) AS total_purchase 
FROM users u JOIN orders o
ON u.id=o.user_id 
JOIN payments p 
ON o.id=p.order_id 
GROUP BY u.id;


SELECT 
	CASE 
    WHEN order_count>=5 
    THEN 'Loyal' 
    ELSE 'Normal' 
    END AS customer_type,
	COUNT(*) AS customers,
    AVG(total_purchase) AS avg_purchase
FROM(
	SELECT u.id,
	COUNT(o.id) AS order_count ,
	SUM(p.total_amount) AS total_purchase 
	FROM users u JOIN orders o
	ON u.id=o.user_id 
	JOIN payments p 
	ON o.id=p.order_id 
	GROUP BY u.id
) AS t
GROUP BY customer_type;





