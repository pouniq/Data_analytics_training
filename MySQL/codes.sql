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
SELECT * FROM users WHERE location IN('Iran', 'UK');




-- index

CREATE INDEX lindex ON users(location);
DROP INDEX lindex ON users;

-- foreign key
CREATE table posts (
id INT AUTO_INCREMENT,
user_id INT,
title VARCHAR(100),
body TEXT,
publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (id),
FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO posts (user_id, title, body) VALUES
(1, 'Getting Started with Python', 'Python is a great language for beginners and data scientists.'),
(1, 'Introduction to Data Science', 'Data science combines statistics, programming, and domain knowledge.'),
(6, 'Learning SQL', 'SQL is an essential skill for working with relational databases.'),
(6, 'Why Statistics Matters', 'Statistics helps us understand data and make better decisions.'),
(7, 'Machine Learning Basics', 'Machine learning allows computers to learn patterns from data.'),
(7, 'Building Better Habits', 'Small and consistent improvements can lead to great results over time.'),
(8, 'My First Project', 'I recently completed my first programming project and learned a lot from it.'),
(8, 'Useful Programming Tips', 'Writing clean and simple code makes projects easier to understand and maintain.');

SELECT * FROM posts;

/*JOIN*/
-- inner join
SELECT * FROM posts INNER JOIN users ON users.id = posts.user_id;
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p INNER JOIN users AS u ON u.id = p.user_id;

-- right join
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p RIGHT JOIN users AS u ON u.id = p.user_id;

-- left join
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p LEFT JOIN users AS u ON u.id = p.user_id;



SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p RIGHT JOIN users AS u ON u.id = p.user_id WHERE p.id IS NULL;

-- make comment table
CREATE TABLE comments (
id INT AUTO_INCREMENT,
post_id INT,
user_id INT,
body TEXT,
publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(id),
FOREIGN KEY(post_id) REFERENCES posts(id),
FOREIGN KEY(user_id) REFERENCES users(id)
);
SELECT * FROM comments;
-- SELECT * FROM posts;
SELECT * FROM users;
-- INSERT INTO comments(post_id, user_id, body) VALUES 
-- (1,1,'comment 1'),
-- (2,8,'comment 2');

SELECT p.title, c.body, u.first_name, u2.id, u2.first_name AS post_user_name
FROM comments AS c 
RIGHT JOIN posts AS p ON p.id = c.post_id
INNER JOIN users AS u ON p.user_id = u.id
INNER JOIN users AS u2 ON p.user_id = u2.id
WHERE u.first_name = 'Amir';



SELECT COUNT(*) FROM posts;

SELECT MAX(age) AS max_age FROM users;
SELECT MIN(age) AS min_age FROM users;

SELECT SUM(age) AS sum_age FROM users;

SELECT gender, COUNT(*) FROM users GROUP BY gender;
SELECT gender, MIN(age), MAX(age), COUNT(*) FROM users GROUP BY gender;


SELECT location,MIN(age), MAX(age), COUNT(*) FROM users GROUP BY location;

SELECT 
CASE WHEN login_count IS NULL THEN 0 
WHEN login_count = 0 THEN '00'
ELSE login_count 
END AS logincount,
COUNT(*)
FROM users 
GROUP BY login_count;




SELECT u.* , CASE WHEN p.post_count IS NULL THEN 0 ELSE p.post_count END FROM users AS u LEFT JOIN 
(SELECT user_id,COUNT(*) AS post_count FROM posts GROUP BY user_id) AS p ON u.id = p.user_id; 













