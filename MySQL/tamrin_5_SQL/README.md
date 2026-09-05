
# تمرین پنجم


## معرفی

این مخزن، تمرین پنجم از مدرسه تحلیل داده است که در آن یک پایگاه‌داده رابطه‌ای در MySQL برای فروشگاه کتاب‌های کمیاب کهن‌نگار طراحی و پیاده‌سازی شده است. پروژه شامل ساخت دیتاست شبیه‌سازی‌شده، رفع چند اشکال ساختاری در schema و اسکریپت تولید داده، و پاسخ به نه پرسش تحلیلی درباره‌ی فروش، مشتریان، محصولات، دسته‌بندی‌ها، کانال‌های فروش و تأثیر تخفیف‌هاست. هر پرسش با یک کوئری SQL، توضیح تصویری از کد SQL و خروجی CSV مستندسازی شده و در کنار آن، مسیر رفع اشکال‌ها (از خطاهای foreign key گرفته تا ناسازگاری نوع داده‌ها) به‌عنوان یک لاگ عیب‌یابی ثبت شده است.



### معرفی فایل ها:

- در فولدر `DatasetGenerator` فایل های درست کردن دیتابیس قرار دارد.
- فولدر `dataset_solutions`، جواب نهایی سوالات را در قالب csv قرار داده.
- فولدر `db` فایل های Database، در دو فرمت csv و sql قرار گرفته است.
- فولدر `pics`، عکس های این README.md را قرار دادم.
- فایل `prompt_tamrin_5.pdf` فایل پرامپت ساخت کد پایتون است.
- فایل `solutions_practice_5.sql` کدهای جواب SQL است.







## نمودار ER برای دیتابیس



![1](<./pics/kohanNegarER.png>) 



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
که id رو از for loop حذف کردم تا بتوانم در SQL واردشون کنم.

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

از برنامه DBeaver کمک گرفتم، بعد از متصل شدن به MySQL، کلیک راست روی دیتابیس میکنیم بعد میریم به قسمت Tools, بعد new task, سپس با استفاده از پنجره ای که در اختیارمون قرار میگیره به فرمت دلخواه از دیتابیس خروجی میگیریم، که من در دو فایل csvو sql خروجی گرفتم.

### مشکل دهم

وقتی روی reverse engineer میزنم MySQLworkbench ، کرش میکنه و یک دفعه ای بسته میشه

#### راه حل:

برای خروجی گرفتن و ساختن ER، چون MySQLworkbench متوقف میشد و crash میکرد، از برنامه DBeaver استفاده کردم، که با متصل شدن به MySQL توسط DBeaver تمام دیتابیس ها وارد DBeaver شدن و در این برنامه نمودار را رسم کردم.



### مشکل یازدهم

```SQL
'categories', 'CREATE TABLE `categories` (\n  `id` int NOT NULL AUTO_INCREMENT,\n  `title` varchar(100) DEFAULT NULL,\n  `parent_id` int DEFAULT NULL,\n  PRIMARY KEY (`id`),\n  KEY `cat_f1_idx` (`parent_id`),\n  CONSTRAINT `cat_f1` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`)\n) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3'
```


این ارور نشون میده که من FK برای جدول `products` رو درست ست نکرده بودم، نیاز بود که REFERENCED TABLE جدول category باشه و از category_id به کلید id در category حرکت کنه.



## جواب ها




### سوال اول




مبلغ فروش را نمايش دهيد. بگوييد كدام ماه بيشترين و كدام ماه كمترين فروش را داشته است. ميزان فروش كسب وكار را به تفكيك ماه محاسبه كنيد. براي هر ماه تعداد سفارشها، تعداد اقلام فروخته شده و مجموع مبلغ فروش را نمايش دهيد. بگوييد كدام ماه بيشترين و كدام ماه كمترين فروش را داشته است.




![1](<./pics/1.jpg>) 




- دیتای به دست آمده از سوال اول:
	- کمترین فروش: ماه February سال 2025
 	- بیشترین فروش: ماه August سال 2025
  
[solution one data](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/1.csv)


### سوال دوم



مشترياني را شناسايي كنيد كه در بازه زماني موردنظر بيش از يك سفارش داشته اند. براي هر مشتري تعداد سفارشها، مجموع مبلغ خريد و ميانگين مبلغ هر سفارش را محاسبه و مشتريان را بر اساس مجموع خريد از بيشترين به كمترين  مرتب كنيد .


![2](<./pics/2.jpg>) 



این افراد با این آیدی ها، ارزشمندترین مشتریان کسب و کار هستند و میتوانیم جشنواره ها و امتیازهای خاص برای این افراد در نظر بگیریم.



'492'


'1370'


'796'


'1061'


'334'


'1267'



[solution two data](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/2.csv)



### سوال سوم






براي هر محصول، تعداد دفعات فروش، مجموع تعداد فروخته شده و مجموع درآمد حاصل از فروش را محاسبه كنيد. سپس ١٠ محصول برتر از نظر درآمد را مشخص كنيد.


![3](<./pics/3.jpg>) 


جواب :


[solution three](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/3.csv)



### سوال چهارم




با استفاده از ارتباط بين جداول محصولات و دستهبندي ها، عملكرد هر دسته را بررسي كنيد. براي هر دسته تعداد محصولات، تعداد اقلام فروخته شده و مجموع درآمد را محاسبه كنيد و مشخص كنيد كدام دسته بيشترين سهم را در درآمد كسب و كار دارد.



![4](<./pics/4.jpg>) 


جواب:


بیشترین سهم از فروش را
'Classical Persian Poetry'
اشعار کلاسیک فارس

دارد.

جواب کامل:



[solution four](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/4.csv)



### جواب پنجم:





عملكرد كانالهاي مختلف فروش را با يكديگر مقايسه كنيد. براي هر كانال تعداد سفارشها، تعداد مشتريان، مجموع فروش و ميانگين ارزش سفارش را محاسبه كنيد. در نهايت مشخص كنيد كدام كانال عملكرد بهتري دارد .



![5](<./pics/5.jpg>) 


جواب:


فروش  با کانال آنلاین عملکرد بهتری نسبت به کانال فروش حضوری داشته.

جواب کامل:

[solution five](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/5.csv)




### جواب ششم:





مشتريان را بر اساس شهر گروهبندي كنيد و براي هر شهر تعداد مشتريان، تعداد سفارشها، مجموع مبلغ خريد و ميانگين خريد هر مشتري را محاسبه كنيد. سپس مشخص كنيد كدام شهر بيشترين ارزش اقتصادي را براي كسبوكار ايجاد كرده است .



![6](<./pics/6.jpg>) 

جواب:


مشتریان از شهر رشت بیشترین خرید را داشتند با میانگین فروش ۹۹ میلیون تومان



[solution six](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/6.csv)


### جواب هفتم:





سفارشها يا پرداختهاي داراي تخفيف را با سفارشها يا پرداختهاي بدون تخفيف مقايسه كنيد. براي هر گروه تعداد تراكنشها، مجموع مبلغ قبل از تخفيف، مجموع مبلغ تخفيف و مجموع مبلغ نهايي را محاسبه كنيد. سپس بررسي كنيد تخفيف چه تأثيري بر مبلغ فروش داشته است .



![7](<./pics/7.jpg>) 



برای بررسی اثر تخفیف روی قیمت اصلی میتوانید این دیتاست رو نگاه کنید.


[solution seven](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/7.csv)



### جواب هشتم:


مشترياني را پيدا كنيد كه در بازه زماني موردنظر هيچ سفارشي نداشته ند يا تعداد سفارش بسيار كمي داشته اند. تعداد اين مشتريان را محاسبه و در صورت امكان آنها را بر اساس شهر و وضعيت فعال/غيرفعال مقايسه كنيد. سپس يك پيشنهاد كسبوكاري براي افزايش مشاركت اين گروه ارائه دهيد .



![8](<./pics/8.jpg>) 



جواب:


[solution eight](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/8.csv)


پیشنهاد:

در رشت با توجه به اینکه بیش از نیمی از این گروه (که خودش نیمی از کل مشتریان است) هرگز خرید نکرده‌اند، این افراد احتمالاً یا فقط ثبت‌نام کرده‌اند بدون تکمیل اولین خرید، یا مشتریان قدیمی‌اند که رها شده‌اند. با توجه به تمرکز جغرافیایی مشکل روی رشت:

یک کمپین «اولین خرید» با تخفیف محدودزمانی برای مشتریانی که order_count=0 دارند، مخصوصاً در رشت
برای گروه order_count=1، پیام یادآوری/پیشنهاد شخصی‌سازی‌شده بر اساس محصولی که یک‌بار خریده‌اند، برای تبدیل به مشتری تکرارشونده
بررسی اینکه آیا کانال فروش حضوری در رشت مشکلی دارد (با توجه به یافته‌ی سوال پنجم که آنلاین عملکرد بهتری داشت)


### جواب نهم:




مشتريان وفادار را با ساير مشتريان مقايسه كنيد. براي هر گروه تعداد مشتريان، ميانگين تعداد سفارش به ازاي هر مشتري، ميانگين مبلغ خريد و ميانگين ارزش سفارش را محاسبه كنيد. سپس مشخص كنيد آيا مشتريان وفادار ارزش بيشتري براي كسبوكار ايجاد ميكنند يا خير .




![9](<./pics/9.jpg>) 




با اینکه تعداد مشتریان وفادار نصف مشتریان دیگر است ولی میانگین خرید آنها ۶ برابر دیگر مشتریان است. پس بله مشتریان وفادار ارزش بیشتری به کسب و کار می دهند.


جواب:


[solution nine](https://github.com/pouniq/Data_analytics_training/blob/main/MySQL/tamrin_5_SQL/dataset_solutions/9.csv)




## منابع اضافه

[ویدیو یادآوری JOIN](https://www.youtube.com/watch?v=G3lJAxg1cy8)

[نحوه خروجی گرفتن از دیتابیس](https://www.youtube.com/watch?v=lbrVhjnM5MQ)

[خروجی گرفتن نمودار توسط DBeaver](https://www.youtube.com/watch?v=pmiTJZpoDJk)

