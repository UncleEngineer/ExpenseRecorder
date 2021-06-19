# basicsqlite3.py

import sqlite3

# สร้าง database
conn = sqlite3.connect('expense.sqlite3')
# สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

# สร้าง table ด้วยภาษา SQL
'''
'รหัสรายการ (transactionid) TEXT',
'วัน-เวลา (datetime)' TEXT,
'รายการ'(title) TEXT,
'ค่าใช้จ่าย (expense) REAL (float)',
'จำนวน (quantity)' INTEGER,
'รวม (total) REAL'
'''
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				transactionid TEXT,
				datetime TEXT,
				title TEXT,
				expense REAL,
				quantity INTEGER,
				total REAL
			)""")

def insert_expense(transactionid,datetime,title,expense,quantity,total):
	ID = None
	with conn:
		c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
			(ID,transactionid,datetime,title,expense,quantity,total))
	conn.commit() # การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
	print('Insert Success!')


def show_expense():
	with conn:
		c.execute("SELECT * FROM expenselist")
		expense = c.fetchall() #คำสั่งให้ดึงข้อมูลเข้ามา
		print(expense)

	return expense

insert_expense('2021156454545','วันเสาร์ 2021-06-19','แอปเปิ้ล',45,2,90)
show_expense()


print('success')