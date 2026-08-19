USE first_db;

INSERT INTO users (first_name, last_name, gender, email, location, is_admin, register_date, password, login_count)
VALUES 
('Amir', 'Abdollahpour', 'm', 'abdollahpora@gmail.com', 'Iran', '1', '2026-08-20', '1241', '3'),
('Sara', 'Karimi', 'f', 'SaraEchos@gmail.com', 'Iran', '0', '2026-08-19', '134212', '1'),
('Ahmad', 'Ahmadi', 'm', 'AhmadiAhmad@gmail.com', 'Iran', '0', '2026-08-18', '42341', '2'),
('Ziba', 'Mortezavi', 'f', 'zibaMort@gmail.com', 'Iran', '1', '2026-08-17', '1983914', '4');


SELECT * FROM users;


SELECT * FROM users WHERE is_admin = 1;
SELECT * FROM users WHERE location = 'Iran';

SELECT * FROM users WHERE location = 'Iran' AND gender = 'f';
SELECT * FROM users WHERE NOT (gender = 'f');
SELECT * FROM users WHERE NOT (gender = 'f' AND is_admin = 0);

SELECT * FROM users WHERE login_count < 2;
SELECT * FROM users WHERE login_count IS NULL;
SELECT * FROM users WHERE login_count IS NOT NULL;


SELECT * FROM users;
DELETE FROM users WHERE id = 2 OR id = 3 OR id = 4 OR id = 5;
SELECT * FROM users;


UPDATE users SET email = 'amir@gmail.com' WHERE id = 1;



ALTER TABLE users ADD age VARCHAR(3);
ALTER TABLE users MODIFY age INT;


UPDATE users SET age = 20 where id > 1;


SELECT * FROM users ORDER BY last_name desc;
SELECT * FROM users ORDER BY age desc;
SELECT * FROM users WHERE gender = 'm' ORDER BY age desc;
SELECT * FROM users WHERE gender = 'm' ORDER BY age desc LIMIT 1;


SELECT id AS unique_id, CONCAT( first_name,' ', last_name) AS full_name FROM users;

SELECT * FROM users WHERE age BETWEEN 20 AND 30;
SELECT * FROM users WHERE first_name LIKE 'A%';

SELECT * FROM users WHERE email LIKE '%.com';
SELECT * FROM users WHERE location IN('Iran', 'UK);














