# import all modules
from tkinter import *
import tkinter.messagebox
import sqlite3

conn = sqlite3.connect("E:\Store Management System\Database\store.db")
c = conn.cursor()

result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]
class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="Add to the database", font=('arial 40 bold'), fg='darkblue')
        self.heading.place(x=400, y=0)

        #lables and entries for window
        self.name_l = Label(master, text="Enter Product Name", font=('arial 18 bold'))
        self.name_l.place(x=0, y=70)

        self.stock_l = Label(master, text="Enter Stocks ", font=('arial 18 bold'))
        self.stock_l.place(x=0, y=120)

        self.sp_l = Label(master, text="Enter Selling Price ", font=('arial 18 bold'))
        self.sp_l.place(x=0, y=170)

        self.cp_l = Label(master, text="Enter Cost Price ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=220)

        self.vendor_l = Label(master, text="Enter Vendor Name ", font=('arial 18 bold'))
        self.vendor_l.place(x=0, y=270)

        self.vendor_phno_l = Label(master, text="Enter Vendor Phone Number ", font=('arial 18 bold'))
        self.vendor_phno_l.place(x=0, y=320)

        self.id_l = Label(master, text="Enter ID ", font=('arial 18 bold'))
        self.id_l.place(x=0, y=370)

        #entries for each labels
        self.name_e = Entry(master, width=25, font=('arial 18 bold'))
        self.name_e.place(x=380, y=70)

        self.stock_e = Entry(master, width=25, font=('arial 18 bold'))
        self.stock_e.place(x=380, y=120)

        self.sp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.sp_e.place(x=380, y=170)

        self.cp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.cp_e.place(x=380, y=220)

        self.vendor_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_e.place(x=380, y=270)

        self.vendor_phno_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_phno_e.place(x=380, y=320)

        self.id_e = Entry(master, width=25, font=('arial 18 bold'))
        self.id_e.place(x=380, y=370)

        #button
        self.btn_add = Button(master, text="Add To Database", width=25, height=2, bg='darkblue', fg='white', command= self.get_items)
        self.btn_add.place(x=520, y=420)

        self.btn_clear = Button(master, text="Clear All Fields", width=18, height=2, bg='darkgreen', fg='white', command=self.clear_all)
        self.btn_clear.place(x=350, y=420)

        #text box for the logs
        self.tBox = Text(master, width=60, height=18)
        self.tBox.place(x=750, y=70)
        self.tBox.insert(END, "ID has reached upto: " + str(id))

        self.master.bind('<Return>', self.get_items)
        self.master.bind('<Up>', self.clear_all)

    def get_items(self, *args, **kwargs):
        # get data from the entries
        self.name = self.name_e.get()
        self.stock = self.stock_e.get()
        self.sp = self.cp_e.get()
        self.cp = self.sp_e.get()
        self.vendor = self.vendor_e.get()
        self.vendor_phno = self.vendor_phno_e.get()

        # dynamic entries.....
        self.totalsp = float(self.sp) * float(self.stock)
        self.totalcp = float(self.cp) * float(self.stock)
        self.assumed_profit = float(self.totalsp - self.totalcp)

        if self.name == '' or self.stock == '' or self.cp == '' or self.sp == '':
            tkinter.messagebox.showinfo("Error", "Please Fill all details")
        else:
            sql = "INSERT INTO inventory (name, stock, sp, cp, totalsp, totalcp, assumed_profit, vendor, vendor_phno)" \
                  " VALUES(?,?,?,?,?,?,?,?,?)"
            c.execute(sql, (self.name, self.stock, self.sp, self.cp, self.totalsp, self.totalcp, self.assumed_profit,
                            self.vendor, self.vendor_phno))
            conn.commit()
            # textbox insert
            self.tBox.insert(END, "\n\n Inserted " + str(self.name) + " into the database with code " + str(self.id_e.get()))

            tkinter.messagebox.showinfo("Success", "Successfully added to the database")


    def clear_all(self, *args, **kwargs):
        self.name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.sp_e.delete(0, END)
        self.cp_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phno_e.delete(0, END)
        self.id_e.delete(0, END)

root = Tk()
b = Database(root)
root.geometry("1366x768+0+0")
root.title("Add to Database")
root.mainloop()
