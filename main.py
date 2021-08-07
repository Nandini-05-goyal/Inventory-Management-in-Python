import datetime
import random
from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime
import math
import os  # os helps python modules to interact with the operating system.provides fetching of contents, identifying current working directory
import random

conn = sqlite3.connect("E:\Store Management System\Database\store.db")
c = conn.cursor()

#date
date = datetime.datetime.now().date()

#temporary lists like sessions
products_list = []
products_price = []
products_quantity = []
products_id = []

# list for labels
labels_list = []
class Application:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        # frames
        self.left = Frame(master, width=700, height=768, bg='white')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=666, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        #components
        self.heading = Label(self.left, text="NIRMAL COSMETICS", font=('arial 40 bold'), bg='white')
        self.heading.place(x=0, y=0)

        self.date_1 = Label(self.right, text="Today's Date : " + str(date), font=('arial 15 bold'), bg='lightblue', fg='black')
        self.date_1.place(x=0, y=0)

        #table invoice....................
        self.tproduct = Label(self.right, text="Products", font=('arial 18 bold'), bg='lightblue', fg='black')
        self.tproduct.place(x=0, y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('arial 18 bold'), bg='lightblue', fg='black')
        self.tquantity.place(x=300, y=60)

        self.tamount = Label(self.right, text="Amount", font=('arial 18 bold'), bg='lightblue', fg='black')
        self.tamount.place(x=500, y=60)

        # enter the details
        self.enterid = Label(self.left, text="Enter Product's id", font=('arial 18 bold'), bg='white')
        self.enterid.place(x=0, y=80)

        self.enteride = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enteride.place(x=190, y=80)
        self.enteride.focus()

        #buttons...
        self.search_btn = Button(self.left, text="Search", width=25, height=2, bg='darkblue', fg='white', command=self.print)
        self.search_btn.place(x=350, y=120)

        #filling details in columns by function print
        self.productname = Label(self.left, text="", font=('arial 20 bold'), bg='white', fg='darkblue')
        self.productname.place(x=0, y=250)

        self.price = Label(self.left, text="", font=('arial 20 bold'), bg='white', fg='darkblue')
        self.price.place(x=0, y=290)

        #total label
        self.total_l = Label(self.right, text="", font=('arial 40 bold'), bg='steelblue', fg='white')
        self.total_l.place(x=0, y=600)

        #bind total label
        self.master.bind("<Return>", self.print)  #bind helps in providing an IP address and port no. to socket instance.
        self.master.bind("<Up>", self.add_to_cart)
        self.master.bind("<space>", self.generate_bill)

    def print(self, *args, **kwargs):
        self.get_id = self.enteride.get()
        #getting products info
        query = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(query, (self.get_id, ))
        for self.r in result:
            self.get_id = self.r[0]
            self.get_name = self.r[1]
            self.get_price = self.r[3]
            self.get_stock = self.r[2]
        self.productname.configure(text="Product's name: " + str(self.get_name))
        self.price.configure(text="Price: " + str(self.get_price))

        #create quantity label
        self.quantity_l= Label(self.left, text="Enter Quantity: ", font=('arial 18 bold'), bg='white')
        self.quantity_l.place(x=0, y=370)

        self.quantity_e= Entry(self.left, width=25, font=('arial 20 bold'), bg='steelblue')
        self.quantity_e.place(x=190, y=370)
        self.quantity_e.focus()

        #create discount label
        self.discount_l = Label(self.left, text="Enter Discount: ", font=('arial 18 bold'), bg='white')
        self.discount_l.place(x=0, y=410)


        self.discount_e = Entry(self.left, width=25, font=('arial 20 bold'), bg='steelblue')
        self.discount_e.place(x=190, y=410)
        self.discount_e.insert(END, 0)

        #add things to cart button
        self.add_to_cart_btn = Button(self.left, text="Add to Cart", width=25, height=2, bg='darkblue', fg='white',
                                      command=self.add_to_cart)
        self.add_to_cart_btn.place(x=350, y=460)

        #generate bill and change
        self.change_l = Label(self.left, text="Given Amount", font=('arial 18 bold'), bg='white')
        self.change_l.place(x=0, y=510)

        self.change_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='steelblue')
        self.change_e.place(x=190, y=510)

        #change button
        self.change_btn = Button(self.left, text="Calculate Change", width=22, height=2, bg='darkblue', fg='white',
                                 command=self.change_money)
        self.change_btn.place(x=350, y=550)

        #generate bill button
        self.generate_bill_btn = Button(self.left, text="Generate Bill", width=30, height=2, bg='red', fg='white',
                                        command=self.generate_bill)
        self.generate_bill_btn.place(x=350, y=600)

    def add_to_cart(self, *args, **kwargs):
        #getting quantity value from database
        self.quantity_value = int(self.quantity_e.get())
        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo("Error", "not too many products in inventory")
        else:
            #calculate the price
            self.final_price = (float(self.quantity_value) * float(self.get_price)) - (float(self.discount_e.get()))

            products_list.append(self.get_name)
            products_price.append(self.final_price)
            products_quantity.append(self.quantity_value)
            products_id.append(self.get_id)

            self.x_index = 0
            self.y_index = 100
            self.counter = 0
            for self.p in products_list:
                self.tempname = Label(self.right, text=str(products_list[self.counter]), font=('arial 18 bold'), bg='steelblue', fg='white')
                self.tempname.place(x=0, y=self.y_index)
                labels_list.append(self.tempname)

                self.tempqnty = Label(self.right, text=str(products_quantity[self.counter]), font=('arial 18 bold'), bg='steelblue',
                                      fg='white')
                self.tempqnty.place(x=300, y=self.y_index)
                labels_list.append(self.tempqnty)

                self.tempprice = Label(self.right, text=str(products_price[self.counter]), font=('arial 18 bold'), bg='steelblue',
                                      fg='white')
                self.tempprice.place(x=500, y=self.y_index)
                labels_list.append(self.tempprice)

                self.y_index += 40
                self.counter += 1

                #total configure
                self.total_l.configure(text="Total: " + str(sum(products_price)))

                #delete configure
                self.quantity_l.place_forget()
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.productname.configure(text="")
                self.price.configure(text="")
                self.add_to_cart_btn.destroy()

                #autofill the enter id
                self.enteride.focus()
                self.enteride.delete(0, END)

    def change_money(self, *args, **kwargs):
        # get change money after customer pays
        self.amount_given = float(self.change_e.get())    #amount given by the customer to purchase the items
        self.calc_total = float(sum(products_price))     #computer calculated total

        self.to_return = self.amount_given - self.calc_total

        # label change
        self.c_amount = Label(self.left, text="Change : Rs. " + str(self.to_return), font=('arial 18 bold'), fg='red')
        self.c_amount.place(x=0, y=600)

    def generate_bill(self, *args, **kwargs):
        # creating the bill at last before updating the db
        directory = "E:/Store Management System/INVOICE/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # templates
        company = "\t\t\t\t NIRMAL COSMETICS \n"
        address = "\t\t\t\t 18-MALIYAN STREET, ARHAT BAZAR, DEHRADUN \n"
        phone = "\t\t\t\t 9897214990 \n"
        sample = "\t\t\t\t INVOICE \n"
        dt = "\t\t\t\t " + str(date)

        table_header = "\n\n\t-----------------------------------------------------------\n\t\t\tSN.\t\tProducts\t\tQuantity\t\tAmount\n\t-----------------------------------------------------------"
        final = company + address + phone + sample + dt + "\n" + table_header

        # open a file to write into it
        file_name = str(directory) + str(random.randrange(5000, 10000)) + ".rtf"
        f = open(file_name, 'w')
        f.write(final)
        # fill dynamics
        r = 1
        i = 0
        for t in products_list:
            f.write("\n\t\t\t" + str(r) + "\t\t\t" + str(products_list[i] + ".....")[:7] + "\t\t\t" + str(products_quantity[i]) + "\t\t\t" + str(products_price[i]))
            i += 1
            r += 1
        f.write("\n\n\t\t\t Total: Rs. " + str(sum(products_price)))
        f.write("\n\t\t\t Thanks for Visiting.....")
        os.startfile(file_name, "print")
        f.close()

        # decreasing the stock
        self.x = 0

        initial = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(initial, (products_id[self.x], ))

        for i in products_list:
            for r in result:
                self.old_stock = r[2]
            self.new_stock = int(self.old_stock) - int(products_quantity[self.x])

            # updating the stock
            sql = "UPDATE inventory set stock=? WHERE id=?"
            c.execute(sql, (self.new_stock, products_id[self.x]))
            conn.commit()

            # insert into the transaction
            sql2 = "INSERT INTO transactions (product_name, quantity, amount, date) VALUES (?, ?, ?, ?)"
            c.execute(sql2, (products_list[self.x], products_quantity[self.x], products_price[self.x], date))
            conn.commit()

            self.x += 1

        for a in labels_list:
            a.destroy()

        del(products_list[:])
        del(products_id[:])
        del(products_quantity[:])
        del(products_price[:])

        self.total_l.configure(text="")
        self.c_amount.configure(text="")
        self.change_e.delete(0, END)
        self.enteride.focus()
        tkinter.messagebox.showinfo("Success", "Done everything smoothly")

root = Tk()
b = Application(root)

root.geometry("1366x768+0+0")
root.mainloop()
