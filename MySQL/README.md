# SQL
## Database:
مجموعه ای از داده ها که به صورت مرتب دسته بندی شده تا بتونیم بهتر به آنها دسترسی داشته باشیم.
برای مدیریت این نوع داده ها از DBMS ها استفاده می شود


زبان برای این نوع داده ها SQL است.


-> MySQL

هر جدول یک اسمی داره.

و ممکن است که یک جدول، دارای کلید دیگر جدول را داشته باشد که به آن foreign key گفته می شود تا بتوان به عنوان مثال از جدول order ، اطلاعات کاربر را از user_key دریافت کنیم.

## Codes:

در MySQL استاندارد این هست که اسم های جداول را با حروف کوچک و اگر بیشتر از یک کلمه بود با _ جدا کنیم به عنوان مثال login_users.



برای ساختن دیتابیس جدید از آیکون create a new schema استفاده می کنیم و با توجه به نیازی که داریم هر ستون را می سازیم.


بعد از اینکه دیتابیس خودمون رو ساختیم میتونیم با :
``` SQL
USE first_db;
```

استفاده کنیم تا از اون دیتابیس استفاده کنه.

بعد از اون برای اینکه جدول خودمون رو از اون دیتابیس انتخاب کنیم از :

``` SQL
SELECT * FROM users
```

استفاده می کنیم تا جدول مورد نظر رو انتخاب کنیم.

### چگونه record به جدول خودمون اضافه کنیم؟

برای اضافه کردن سطر به جدول خودمون می تونیم به صورت دستی وارد کنیم یا به صورت کد :

برای وارد کردن داده ها به صورت کد نیاز هست که از این دستور استفاده کنیم:



در وارد کردن داده ها نمی توان از "" استفاده کرد (یعنی double quotation ) باید از single quotation یعنی '' استفاده کرد.


``` SQL
INSERT INTO users (first_name, last_name, gender, email, location, is_admin, register_date, password, login_count) VALUES ('Amir', 'Abdollahpour', 'm', 'abdollahpora@gmail.com', 'Iran', '1', '2026-08-20', '1241', '3')
```

در ورژن جدید MySQL برای نشان دادن datetime به جای استفاده از / از - استفاده می شود.



### فیلتر کردن دیتاست:

برای فیلتر کردن دیتاست خودمون از دستور **WHERE** استفاده می کنیم به عنوان مثال برای پیدا کردن کسانی که ادمین هستند از این کد استفاده می کنیم:

``` SQL
SELECT * FROM users WHERE is_admin = 1;
```


یا برای فیلتر کردن کسانی که در ایران زندگی میکنند می توانیم از این کد استفاده کنیم:


``` SQL
SELECT * FROM users WHERE location = 'Iran';

```

حالا می توانیم این نوع فیلتر کردن ها رو پیچیده تر کنیم:
1. AND:
یا (و) خودمون که باید هر دو همزمان درست باشند تا در خروجی به ما نشان داده شود.

```SQL
SELECT * FROM users WHERE location = 'Iran' AND gender = 'f';
```


3. OR
یا همان (یا) خودمون که هر کدام از شروط درست باشد آن را با خروجی می دهد.
4. NOT
```SQL
SELECT * FROM users WHERE NOT (gender = 'f');
```
حالت منفی آن عبارت منطقی را در نظر می گیرد.

زمانی NOT کاربرد خودش رو نشون میده که ما چندین عبارت منطقی داشته باشیم که بخواهیم نقیض تمام آن ها را در نظر بگیریم.

``` SQL
SELECT * FROM users WHERE NOT (gender = 'f' AND is_admin = 0);
```
مانند اینجا که خانم ها یا کسانی که ادمین نیستند **انتخاب نشده اند.** یا به عبارتی خانم هایی که ادمین نیستند.


### مقایسه ها ریاضی:
>   greater than
>=  greater than or equal
<   less than
<=  less than or equal
=   equal
<>  not equal
!=  not equal (MySQL supports this)


که می توانیم در WHERE از آنها استفاده کنیم.
``` SQL
SELECT * FROM users WHERE login_count < 2;
```

اما برای مقادیر NULL نمی شود از مقایسه های ریاضی استفاده کرد باید از IS NULL استفاده شود.
```SQL
SELECT * FROM users WHERE login_count IS NULL;
```

 و برای بررسی اینکه NULL نیستند از این کد استفاده می کنیم.
```SQL
SELECT * FROM users WHERE login_count IS NOT NULL;
```



### حذف یک سطر یا record از دیتاست:

از این کد استفاده می کنم برای اینکه record ها تکراری که داشتم را حذف حتما راه راحتری برای این موضوع هست :

```SQL
DELETE FROM users WHERE id = 2 OR id = 3 OR id = 4 OR id = 5;
```
میتوانیم بر اساس تمام field های که داریم record هایی که داریم را حذف کنیم. 

### آپدیت کردن :

می دانیم که می شود به صورت دستی اینکار را انجام داد حالا اگر بخواهیم به صورت دستوری این کار را انجام دهیم از این دستور استفاده می کنیم.

در این کد داریم میگیم که آپدیت کن در دیتاست users ایمیل رو به چیزی که مد نظر داریم با توجه به اینکه id آن record برابر ۱ باشد.





```SQL
UPDATE users SET email = 'amir@gmail.com' WHERE id = 1;
```


### اضافه کردن field یا ستون جدید به دیتاست:

برای ساختن ستون جدید از این کد استفاده می کنیم:
```SQL
ALTER TABLE users ADD age VARCHAR(3);

```

زمانی که میخوایم هر field رو تغییرات روش اعمال کنیم از MODIFY استفاده می کنیم.
```SQL
ALTER TABLE users MODIFY age INT;
```


### مقدار دهی که field ها:

این کد برای تمام id های بیشتر از ۱ برای ستون age عدد ۲۰ را جایگذاری میکنه.

که می تونیم به صورت دستی هم مقدار دهی کنیم.

```SQL
UPDATE users SET age = 20 where id > 1;
```



### مرتب کردن بر اساس ستون دلخواه:

میتوانیم از ORDER BY استفاده کنیم تا بر اساس هر ستونی که میخواهیم دیتاست را خروجی بگیریم.

که عبارت آخر می تواند asc یا به معنای صعودی یا desc به معنای نزولی باشد.

میتوانیم از LIMIT نیز استفاده کنیم تا تعداد record ها خروجی را محدود کنیم.
```SQL
SELECT * FROM users ORDER BY last_name desc;
SELECT * FROM users ORDER BY age desc;
SELECT * FROM users WHERE gender = 'm' ORDER BY age desc;
SELECT * FROM users WHERE gender = 'm' ORDER BY age desc LIMIT 1;
```


### وصل کردن دو مقدار ستون بهم:

برای اینکه به عنوان مثال یک ستون برای نام و نام خانوادگی داشته باشیم نیاز هست که دو ستون نام و بعد نام خانوادگی را بهم دیگر وصل کنیم در اینجا می توانیم از تابع CONCAT استفاده کنیم و باید یک نام نیز برای ستون ساخته شده نیز بعد از AS انتخاب کنیم که در اینجا `full_name` هست.



```SQL
SELECT id AS unique_id, CONCAT( first_name,' ', last_name) AS full_name FROM users;
```



برای فیلتر کردن پیشرفته تر می توانیم بگوییم که سن هایی که بین ۲۰ تا ۳۰ هستند را فقط به ما نمایش بده که به وسیله BETWEEN قابل انجام هست.
```SQL
SELECT * FROM users WHERE age BETWEEN 20 AND 30;
```


### استفاده از LIKE:

به عنوان مثال برای پیدا کردن تمام نام هایی که با A شروع می شود می توانیم از کد پایین استفاده کنیم و یا ایمیل هایی که با .com تمام می شود.

```SQL
SELECT * FROM users WHERE first_name LIKE 'A%';

SELECT * FROM users WHERE email LIKE '%.com';
```



یک دیگر از روش های فیلتر کردن استفاده از IN هست که میتوانیم بگوییم تمام کاربرانی که یا در ایران هستند یا در انگلستان هستند را به ما نشون بده.
```SQL
SELECT * FROM users WHERE location IN('Iran', 'UK');

```


### ساختن و حذف index:

برای ساختن index از CREATE INDEX استفاده می کنیم.

برای حذف کردن index از DROP INDEX استفاده می کنیم.

```SQL
CREATE INDEX lindex ON users(location);
DROP INDEX lindex ON users;
```


## ساختن جدول posts:

در کد پایین ما یک جدول دیگر به نام `posts` را ساختیم که دارای field های، id برای خود همان جدول `posts` در گام بعدی یک *Foreign Key* ساختیم که دو جدول `users` و `posts` رو به هم دیگه وصل کنه. برای هر پست خودمون نیاز داریم که یک عنوان داشته باشیم که با VARCHAR(100) ستون عنوان را ساختیم، برای محتوای هر پست نیز نیاز به یک ستون داریم که از text استفاده شد، بعد زمان انتشار پست.

بعد از اینکه ستون ها را تعریف کردیم باید PK و FK را نیز تعیین کنیم.
/

```SQL

CREATE table posts (
id INT AUTO_INCREMENT,
user_id INT,
title VARCHAR(100),
body TEXT,
publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (id),
FOREIGN KEY (user_id) REFERENCES users(id)
) 


```

## فیلتر کردن همزمان دو جدول:
برای این کار نیاز به **JOIN** کردن داریم:

سه نوع JOIN در اینجا معرفی شده:
1. INNER JOIN
فقط رکوردهایی را برمی‌گرداند که در هر دو جدول تطابق داشته باشند. به عنوان مثال:

در اینجا ما دو جدول، `posts` و `users` را در کنار هم بر اساس id در جدول `users` و foreign key در جدول `posts` کنار هم قرار می دهیم.
```SQL

SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p INNER JOIN users AS u ON u.id = p.user_id;

```

2. RIGHT JOIN

در RIGHT JOIN، آن جدولی که سمت راست قرار دارد یعنی در اینجا `users` تمامش باقی می ماند و مشترک های `posts` در کنار آن قرار می گیرد.

```SQL
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p RIGHT JOIN users AS u ON u.id = p.user_id;
```

تمام user ها رو نگه میداره و مطابق همون کسانی که پست گذاشتن را به ما خروجی میده و اگر پستی نگذاشته باشند به ما NULL بر می گرداند.

که می توانیم با این کد آن ها را پیدا کنیم.


```SQL
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p RIGHT JOIN users AS u ON u.id = p.user_id WHERE p.id IS NULL;
```
**تمام رکوردهای جدول سمت راست حفظ می‌شوند.**

3. LEFT JOIN

در LEFT JOIN ، بر خلاف RIGHT JOIN عمل می کند و جدول سمت چپی با جدول سمت راستی تطبیق داده می شود و خروجی به ما میدهد.
یعنی به طور کلی:

**تمام رکوردهای جدول سمت چپ حفظ می‌شوند.**


تمام عنوان های posts را نگه میداره و user هایی که post گذاشتن را به ما خروجی میده.
```SQL
SELECT u.first_name, u.last_name, p.id, p.title FROM posts AS p LEFT JOIN users AS u ON u.id = p.user_id;
```

INNER JOIN → فقط مشترک‌ها

LEFT JOIN  → همه‌ی جدول LEFT + تطابق‌های RIGHT

RIGHT JOIN → همه‌ی جدول RIGHT + تطابق‌های LEFT


## ساختن جدول comments:


ساختن جدول comments و وارد کردن دو ریکورد:

```SQL
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
SELECT * FROM posts;
SELECT * FROM users;
INSERT INTO comments(post_id, user_id, body) VALUES 
(1,1,'comment 1'),
(2,8,'comment 2');
```


### فیلتر کردن سه جدول comments, users, posts:



  در اینجا یک کئوری برای تعیین اینکه چه کسانی پست گذاشتند و چه کسانی کامنت گذاشتن به طوری که کسی که پست گذاشته، کامنت آن فرد را دیگر در نظر نگیره. 


```SQL
SELECT p.title, c.body, u.first_name, u2.id, u2.first_name AS post_user_name
FROM comments AS c 
RIGHT JOIN posts AS p ON p.id = c.post_id
INNER JOIN users AS u ON p.user_id = u.id
INNER JOIN users AS u2 ON p.user_id = u2.id
WHERE u.first_name = 'Amir' AND u2.first_name != 'Amir' ;

```

### استفاده از توابع در کئوری:

- COUNT، شمارش انجام میده
- MAX, ماکزیمم عدد را در نظر میگیره
- MIN, می نیمم عدد را در نظر میگیره
- SUM, ستونهایی عددی را میشود با این تابع باهم جمع زد

```SQL
-- شمارش تعداد پست عا
SELECT COUNT(*) FROM posts;

-- ماکزیمم سن از جدول users
SELECT MAX(age) AS max_age FROM users;

-- می نیمم سن از جدول users
SELECT MIN(age) AS min_age FROM users;


-- جمع تمام سن ها در جدول users
SELECT SUM(age) AS sum_age FROM users;

-- شمارش افراد در هر گروه جنسیت و تعیین ماکزیمم و می نیمم سن هر جنسیت

SELECT gender, COUNT(*) FROM users GROUP BY gender;
SELECT gender, MIN(age), MAX(age), COUNT(*) FROM users GROUP BY gender;

-- گروه بندی بر اساس مکان زندگی
SELECT location,MIN(age), MAX(age), COUNT(*) FROM users GROUP BY location;
```



## MarketPlace Database

برای ساختن دیتابیس جدید از همان شیوه ای که آموختیم استفاده می کنیم.

برای بالا بردن امنیت دیتابیس برای id به جای استفاده از INT از UUID یا GUID استفاده می کنیم که یک متن ۳۶ کاراکتر سیستم خودش برای ما میسازه که به همین سبب امنیت دیتابیس بالاتر میره.

برای اینکه بتوانیم به یک نفر چندین نفش یا role بدیم نیاز هست که یک جدول میانی نیز بسازیم برای ساختن جدول میانی باید دو تا PK داشته باشیم یکی برای خود آن جدول و دومی برای role_id را نیز PK در نظر بگیریم.


یک نکته مهم این است که باید char set هر کدوم از id ها مانند همدیگه باشند که باید آن ها را مانند هم کنیم بعد آن ها را بهم وصل کنیم.

برای ساختن دسته بندی های کالا در چندین سطح نیاز هست که یک کلید به نام parent_id داشته باشیم که به id خود همون جدول برگرده.


























