USE practice;

SELECT * 
FROM sales;


-- 1:
SELECT *
FROM sales
WHERE Channel = 'Online';

-- 2:
SELECT *
FROM sales
WHERE Quantity > 4;

-- 3:
SELECT SaleID
FROM sales
ORDER BY TotalAmount DESC LIMIT 10;

-- 4:
SELECT COUNT(SaleID)
FROM sales;


-- 5:
SELECT DISTINCT(City)
FROM sales;


-- 6:
SELECT COUNT(Discount) AS NumDiscount
FROM sales
WHERE Discount > 0;


-- 7:
-- card is the most used PaymentMethod
SELECT PaymentMethod, COUNT(PaymentMethod) AS NumPayMethod
FROM sales
GROUP BY PaymentMethod;

-- 8:
SELECT CustomerType,SUM(TotalAmount)
FROM sales
GROUP BY CustomerType;

-- 9:
SELECT *
FROM sales
WHERE TotalAmount > 1000000 
AND City = 'Rasht';


-- 10.1:
SELECT MIN(Date) AS firstDate
FROM sales;

SELECT MAX(Date) AS lastDate
FROM sales;


-- 10.2:

SELECT *
FROM sales
ORDER BY Date DESC LIMIT 1;


SELECT *
FROM sales
ORDER BY Date ASC LIMIT 1;

-- 11:
SELECT City, AVG(TotalAmount) AS TotalByCity
FROM sales
GROUP BY City;

-- 12:
SELECT PaymentMethod, COUNT(PaymentMethod)
FROM sales
GROUP BY PaymentMethod
HAVING COUNT(PaymentMethod) > 50;




















