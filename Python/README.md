# تمرین ششم 


![2](<./images/back.jpg>) 



## درست و فعال کردن محیط مجازی (virtual environment):






ساختن یک محیط مجازی برای نصب کتابخانه های مورد نیاز:
```BASH
python3 -m venv dataAnalytics
```




فعال کردن محیط مجازی برای نصب کتابخانه ها:
```BASH
source dataAnalytics/bin/activate
```



## نصب کتابخانه ها



کتابخانه های مورد نیاز ابتدایی را نصب می کنیم:
- نامپای
- مت پلات لیب
- پانداز
![2](<./images/install_libraries.png>) 




نصب mySQL connector:


![2](<./images/install_mysql.png>) 



نصب کتابخانه dotenv, برای اینکه میخواستم فایل را در گیتهاب منتشر کنم پس نیاز بود که رمز و یوزرنیم را در یک فایل جداگانه قرار می دادم و آن را فراخوانی می کردم و همزمان فایل .env را در .gitignore قرار دادم تا در گیتهاب push نشود.

![2](<./images/install_dotenv.png>) 

## باگ ها:

```python
UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection.
```
پانداز در اینجا هشدار می دهد که باید از SQLAlchemy که یکی دیگر از کتابخانه های پایتون هست و از پانداز هم مشکلی ندارد استفاده کنیم و به دلیل اینکه مشکلی ایجاد نشد از استفاده از SQLAlchemy صرف نظر کردم.




یک باگ دیگر: من order_id رو به عنوان PK در order_detail2 قرار داده بودم که اشتباه بود باید detail_id رو قرار میدادم.



![2](<./images/error_selecting_db.png>) 

به دلیل اینکه چندین دیتابیس درون MySQL من وجود داشت به همین دلیل باید به این صورت مشخص می کردم که کدام دیتابیس را میخواهم.



```python
df = pd.read_sql("SELECT * FROM KohanNegar.order_detail2", conn)
```

