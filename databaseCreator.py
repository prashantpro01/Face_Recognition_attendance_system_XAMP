from pymysql import *
import pymysql.cursors
from datetime import *
conn = connect(host="localhost",user="root",password="")
var = conn.cursor()
var.execute("DROP database IF EXISTS frbas")
var.execute("CREATE database FRBAS")
print("database created")
var.execute("USE frbas")
var.execute("CREATE TABLE attendance (name VARCHAR(20), date DATE, time Time)")