import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

from dotenv import load_dotenv
import os


load_dotenv()

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD')
)



print("USER:", os.getenv("DB_USER"))
print("PASSWORD:", os.getenv("DB_PASSWORD"))

df = pd.read_sql("SELECT * FROM order_detail2", conn)
print(df.head())
print(df.head(10))
print(df.tail()) 