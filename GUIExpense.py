# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
###########DATABASE#############
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
	#print('Insert Success!')

def show_expense():
	with conn:
		c.execute("SELECT * FROM expenselist")
		expense = c.fetchall() #คำสั่งให้ดึงข้อมูลเข้ามา
		#print(expense)

	return expense

def update_expense(transactionid,title,expense,quantity,total):
	with conn:
		c.execute("""UPDATE expenselist SET title=?, expense=?, quantity=?, total=? WHERE transactionid=?""",
			([title,expense,quantity,total,transactionid]))
	conn.commit()
	#print('Data updated')


def delete_expense(transactionid):
	with conn:
		c.execute("DELETE FROM expenselist WHERE transactionid=?",([transactionid]))
	conn.commit()
	#print('Data deleted')
########################




# ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย v.1.0 by Uncle Engineer')
# GUI.geometry('720x700+500+50')

w = 720
h = 700

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 100

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI หลัก

##############MENU###############
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# Help
def About():
	print('About Menu')
	messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BTC ก็พอแล้ว\nBTC Address: abc')


helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

# Donate
def Donate():
	messagebox.showinfo('Donate','dogecoin network: DLaoRTEF36VqfUpLrcWKcrNDKH27VsqJ6v\nDogecoin BEP20(BSC):    0x0fd36bbcf3f1010796e748d3c4bd48c7ee61620e')
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)
#################################


Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 = PhotoImage(file='t1_expense.png') #  .subsample(2) = ย่อรูป
icon_t2 = PhotoImage(file='t2_expenselist.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
#F1.place(x=100,y=50)
F1.pack()

days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัสบดี',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()

	if expense == '':
		#print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return
	elif quantity == '':
		quantity = 1

	total = float(price) * float(quantity)
	try:
		total = float(price) * float(quantity)
		# .get() คือดึงค่ามาจาก v_expense = StringVar()
		#print('รายการ: {} ราคา: {}'.format(expense,price))
		#print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total))
		text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
		text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
		v_result.set(text)
		# clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')

		# บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
		today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
		#print(today)
		stamp = datetime.now()
		dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
		transactionid = stamp.strftime('%Y%m%d%H%M%f')
		dt = days[today] + '-' + dt
		#print(type(transactionid))
		insert_expense(transactionid,dt,expense,float(price),int(quantity),total)

		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
			# newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
			data = [transactionid,dt,expense,price,quantity,total]
			fw.writerow(data)

		# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
		E1.focus()
		update_table()
	except Exception as e:

		print('ERROR:',e)
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')

# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'

#------Image--------

main_icon = PhotoImage(file='icon_money.png')

Mainicon = Label(F1,image=main_icon)
Mainicon.pack()


#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------

#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-------------------

#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------

icon_b1 = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('--------ผลลัพธ์--------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
# result = Label(F1, textvariable=v_result,font=FONT1,fg='green')
result.pack(pady=20)

#################TAB2##################



def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data

# table

L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
# 	resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [120,150,170,80,80,80]
for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)

# resulttable.insert('',0,value=['จันทร์','น้ำดื่ม',30,5,150])
# resulttable.insert('','end',value=['อังคาร','น้ำดื่ม',30,5,150])

alltransaction = {}

def UpdateCSV():
	with open('savedata.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		# เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
		data = list(alltransaction.values())
		fw.writerows(data) # multiple line from nested list [[],[],[]]
		print('Table was updated')

def UpdateSQL():
	data = list(alltransaction.values())
	#print('UPDATE SQL:',data[0])
	for d in data:
		# transactionid,title,expense,quantity,total
		# d[0]=202106122141118807,d[1]เสาร์-2021-06-12 21:41:35,d[2]มะม่วง,d[3]500.0,d[4]1.0,d[5]500.0
		update_expense(d[0],d[2],d[3],d[4],d[5])




def DeleteRecord(event=None):
	check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
	#print('YES/NO:',check)

	if check == True:
		#print('delete')
		select = resulttable.selection()
		#print(select)
		data = resulttable.item(select)
		data = data['values']
		transactionid = data[0]
		#print(transactionid)
		#print(type(transactionid))
		del alltransaction[str(transactionid)] # delete data in dict
		#print(alltransaction)
		#UpdateCSV()
		delete_expense(str(transactionid)) # delete in DB
		update_table()
	else:
		#print('cancel')
		pass

BDelete = ttk.Button(T2,text='Delete',command=DeleteRecord)
BDelete.place(x=50,y=550)

resulttable.bind('<Delete>',DeleteRecord)

def update_table():
	resulttable.delete(*resulttable.get_children())
	# for c in resulttable.get_children():
	# 	resulttable.delete(c)
	try:
		data =  show_expense() #read_csv()
		#print('DATA:',data)
		for d in data:
			#creat transaction data
			alltransaction[d[1]] = d[1:] # d[1] = transactionid
			resulttable.insert('',0,value=d[1:])
		#print('TS:',alltransaction)
	except Exception as e:
		print('No File')
		print('ERROR:',e)


########Right Click Menu#########
def EditRecord():
	POPUP = Toplevel() # คล้ายๆกับ Tk()
	POPUP.title('Edit Record')
	# POPUP.geometry('500x400')
	w = 500
	h = 400

	ws = POPUP.winfo_screenwidth() #screen width
	hs = POPUP.winfo_screenheight() #screen height


	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2) - 100

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	#------text1--------
	L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
	v_expense = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()
	#-------------------

	#------text2--------
	L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
	v_price = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
	E2.pack()
	#-------------------

	#------text3--------
	L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
	v_quantity = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
	E3.pack()
	#-------------------

	def Edit():
		# print(transactionid)
		# print(alltransaction)
		olddata = alltransaction[str(transactionid)]
		#print('OLD:',olddata)
		v1 = v_expense.get()
		v2 = float(v_price.get())
		v3 = float(v_quantity.get())
		total = v2 * v3
		newdata = [olddata[0],olddata[1],v1,v2,v3,total]
		alltransaction[str(transactionid)] = newdata
		#UpdateCSV()
		UpdateSQL()
		# update_expense(olddata[0],olddata[1],v1,v2,v3,total) # single record update
		update_table()
		POPUP.destroy() #สั่งปิด popup


	icon_b1 = PhotoImage(file='b_save.png')

	B2 = ttk.Button(POPUP,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Edit)
	B2.pack(ipadx=50,ipady=20,pady=20)

	# get data in selected record
	select = resulttable.selection()
	#print(select)
	data = resulttable.item(select)
	data = data['values']
	#print(data)
	transactionid = data[0]
	 # สั่งเซ็ตค่าเก่าไว้ตรงช่องกรอก
	v_expense.set(data[2])
	v_price.set(data[3])
	v_quantity.set(data[4])

	POPUP.mainloop()



rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup)


update_table()

#print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()