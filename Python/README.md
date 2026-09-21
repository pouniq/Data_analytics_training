# تمرین ششم 

## باگ ها:

```python
UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection.
```
پانداز در اینجا هشدار می دهد که باید از SQLAlchemy که یکی دیگر از کتابخانه های پایتون هست و از پانداز هم مشکلی ندارد استفاده کنیم و به دلیل اینکه مشکلی ایجاد نشد از استفاده از SQLAlchemy صرف نظر کردم.




یک باگ دیگر: من order_id رو به عنوان PK در order_detail2 قرار داده بودم که اشتباه بود باید detail_id رو قرار میدادم.



به دلیل اینکه چندین دیتابیس درون MySQL من وجود داشت به همین دلیل باید به این صورت مشخص می کردم که کدام دیتابیس را میخواهم.



```python
df = pd.read_sql("SELECT * FROM KohanNegar.order_detail2", conn)
```

