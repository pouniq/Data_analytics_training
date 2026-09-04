
# تمرین پنجم 

## یک ایراد کوچک در دیاگرام صفحه ۳

من خواستم دوباره database رو فقط از روی diagram که صفحه ۳ ارائه شده بسازم که یک نکته ای که متوجه شدم این بود که user_id در جدول user_basket با  VARCHAR(45) وجود داشت ولی در id در جدول users همراه با VARCHAR(40) بود. که user_Id در user_basket را تغییر دادم.



## فایل پرامپت:
فایل پرامپت در `prompt_tamrin_5.pdf` قرار دارد.


یک جمله نیز به prompt اضافه کردم تا مشکلی در خواندن دیتا توسط پایتون و MySQL پیش نیاید:

> [!NOTE] 
> **نکته مهم:** تمام داده‌هايي كه در Dataset توليد مي‌شوند بايد به زبان انگليسي باشند تا مشكلي در `charset` به وجود نيايد.
> 


## باگ هایی که باهاش برخورد کردم:


### مشکل اول
در استفاده از LLM ها، یک ارور برخورد کردم که به جای جدول user_basket  نوشته بود basket_items، که تغییرش دادم.

### مشکل دوم

یک باگ دیگری که کد پایتون داشت، برای جدول user_basket یک id جداگانه هم در نظر گرفته بود که ولی در خود جدول user_basket وجود نداشت به این شکل:

```python
sql_lines.append("\n-- Insert Basket Items")
for i in range(1, num_user_basket + 1):
	user_id = random.randint(1, num_users)
	product_id = random.randint(1, num_products)
	qty = random.randint(1, 3)
	sql_lines.append(f"INSERT INTO user_basket (id <--**, user_id, product_id, quantity) VALUES ({i}, {user_id}, {product_id}, {qty});")
print(f"Generated {num_user_basket} basket items.")

sql_lines.append("\nSET FOREIGN_KEY_CHECKS = 1;")
```
که i رو از for loop حذف کردم تا بتوانم در SQL واردشون کنم.

```python
sql_lines.append("\n-- Insert Basket Items")
for i in range(1, num_user_basket + 1):
	user_id = random.randint(1, num_users)
	product_id = random.randint(1, num_products)
	qty = random.randint(1, 3)
	sql_lines.append(f"INSERT INTO user_basket (user_id , product_id, quantity) VALUES ({user_id}, {product_id}, {qty});")
print(f"Generated {num_user_basket} basket items.")

sql_lines.append("\nSET FOREIGN_KEY_CHECKS = 1;")
```

### مشکل سوم
```SQL
Error Code: 1062. Duplicate entry '1186' for key 'user_basket.PRIMARY'
```

این مشکل به این دلیل بود که باید دو PRIMARY KEY قرار میدادم، هم user_id و هم product_id
به دلیل باگ قبلی چون چندین دفعه دیتا رو وارد کردم الان با مشکل duplicate مواجه شدم از این کد استفاده میکنم تا دیتا رو حذف کنم و بعد دوباره واردشون کنم.

```SQL
DELETE FROM user_basket;
```

اروری که از این کد گرفتم :

```SQL
16:45:20 DELETE FROM user_basket Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect. 0.0058 sec
```

و اینطور حلش کردم:

```SQL
SET SQL_SAFE_UPDATES = 0;

DELETE FROM user_basket;

SET SQL_SAFE_UPDATES = 1;
```


### باگ چهارم



یک باگ دیگه در جدول products ما یک category_id داشتیم که در اینجا به نام category بود که باید این ستون اصلاح می شد.


```python
f.write("-- TABLE: products\n")
for p in products:
	detail_clean = p['detail'].replace("'", "''")
	title_clean = p['title'].replace("'", "''")
	f.write(f"INSERT INTO products (id, title, detail, price, **category**) VALUES ({p['id']}, '{title_clean}', '{detail_clean}', {p['price']}, {p['category_id']});\n")
f.write("\n")
```


که به این صورت تغییر دادم:


```python
f.write("-- TABLE: products\n")
for p in products:
	detail_clean = p['detail'].replace("'", "''")
	title_clean = p['title'].replace("'", "''")
	f.write(f"INSERT INTO products (id, title, detail, price, **category_id**) VALUES ({p['id']}, '{title_clean}', '{detail_clean}', {p['price']}, {p['category_id']});\n")
f.write("\n")
```


### باگ پنجم



``` SQL
01:19:26	INSERT INTO products (id, title, detail, price, category_id) VALUES (179, 'Coastal Antique Echoes Vol. 56', 'A fine collection of antique reprints curated for art and literature connoisseurs. Features high quality printing and detailed annotations.', 150360000, 27)	Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (`kohannegar`.`products`, CONSTRAINT `products_f1` FOREIGN KEY (`id`) REFERENCES `categories` (`id`))	0.00034 sec
```

اینجا  یک مشکل در schema ایجاد کردم که category_id رو Foreign key در product در نظر نگرفتم.

```SQL

ALTER TABLE `KohanNegar`.`products` 
ADD INDEX `prod_f1_idx` (`category_id` ASC) VISIBLE;
;
ALTER TABLE `KohanNegar`.`products` 
ADD CONSTRAINT `prod_f1`
  FOREIGN KEY (`category_id`)
  REFERENCES `KohanNegar`.`categories` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

```


### باگ ششم
در جدول user_roles هم هوش مصنوعی دادها را به جدول roles_user داره وارد میکنه به همین دلیل داده ها به وارد جدول نمیشه.
که اون رو در پایتون کنترل کردم.


### باگ هفتم
جدول در MySQL به نام payment هست ولی در کد به نام payments. که نام جدول رو در MySQL تبدیل به payments کردم.

### باگ هشتم

```SQL
Error Code: 1366. Incorrect integer value: 'card' for column 'payment_type' at row 1
```

این ارور هم میگه که payment_type که روش پرداخت هست، به صورت string هست اما در دیتابیس من این ستون رو integer در نظر گرفته بودم. تبدیل کردم به varchar(10)


### باگ نهم
یک اشتباه دیگر که کردم این بود که discount_id و discount_price رو گذاشته بودم روی not null که می گه این ستون اصلا نمی تونه null باشه. که اون تیک ها رو برداشتم.



### مشکل نهم

زمانی که میخواهم از دیتابیس خروجی بگیریم با data export هیچکدوم از جداولی که ساختم رو نمی تونم ببینیم.

#### راه حل:
فعلا پیدا نکردم.



### مشکل دهم

وقتی روی reverse engineer میزنم MySQLworkbench ، کرش میکنه و یک دفعه ای بسته میشه

#### راه حل:
فعلا پیدا نکردم.



## جواب ها

## توضیحات کد



[solution one](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/1.csv)


![1](<./pics/1.jpg>) 

[solution two](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/2.csv)


![2](<./pics/2.jpg>) 


[solution three](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/3.csv)


![3](<./pics/3.jpg>) 



[solution four](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/4.csv)



![4](<./pics/4.jpg>) 




[solution five](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/5.csv)



![5](<./pics/5.jpg>) 


[solution six](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/6.csv)



![6](<./pics/6.jpg>) 


[solution seven](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/7.csv)



![7](<./pics/7.jpg>) 


[solution eight](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/8.csv)




![8](<./pics/8.jpg>) 


[solution nine](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/9.csv)



![9](<./pics/9.jpg>) 



## منابع اضافه

[ویدیو یادآوری JOIN](https://www.youtube.com/watch?v=G3lJAxg1cy8)

[نحوه خروجی گرفتن از دیتابیس](https://www.youtube.com/watch?v=lbrVhjnM5MQ)

