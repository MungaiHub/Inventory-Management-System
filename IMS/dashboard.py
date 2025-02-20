from tkinter import*
from PIL import Image, ImageTk
from employee import employeeclass
from supplier import  supplierclass
from category import categoryclass
from product import productclass
from sales import salesclass
import sqlite3
from tkinter import messagebox
import time
import os

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("inventory management system | developed by Amos")
        self.root.config(bg="white")

        #====title=======
        self.icon_title=PhotoImage(file="images/cart1.png")
        title=Label(self.root,text="inventory management system", image=self.icon_title, compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white", anchor="w", padx=20).place(x=0,y=0, relwidth=1, height=70)
        

        #====btn_loogout===
        btn_logout=Button(self.root, text="Logout", command=self.logout,font=("times new roman", 15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        
        #===clock======
        self.lbl_clock=Label(self.root,text="welcome to inventory management system\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",  font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70, relwidth=1, height=30)

        #=====left menu====
        self.MenuLogo = Image.open("images/ims2.jpg")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        leftMenu=Frame(self.root,bd=2,relief=RIDGE, bg="white")
        leftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menulogo=Label(leftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(leftMenu, text="Menu", font=("times new roman", 20),bg="#009688").pack(side=TOP,fill=X)


        btn_employee=Button(leftMenu, text="Employee",command=self.employee,image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(leftMenu, text="Supplier",command=self.supplier,image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(leftMenu, text="Category",command=self.category,image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(leftMenu, text="Product",command=self.product,image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(leftMenu, text="Sales",command=self.sales,image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(leftMenu, text="Exit",image=self.icon_side, compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"),bg="white",bd=3, cursor="hand2").pack(side=TOP,fill=X)
        
        #=======content========
        self.lbl_employee=Label(self.root, text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE, bg="#33bbf9",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300,y=120,height=150, width=300)

        self.lbl_supplier=Label(self.root, text="Total Supplier\n[ 0 ]",bd=5,relief=RIDGE, bg="#ff5722",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650,y=120,height=150, width=300)
        
        self.lbl_category=Label(self.root, text="Total Category\n[ 0 ]",bd=5,relief=RIDGE, bg="#009688",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000,y=120,height=150, width=300)

        self.lbl_product=Label(self.root, text="Total Product\n[ 0 ]",bd=5,relief=RIDGE, bg="#607d8b",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300,y=300,height=150, width=300)

        self.lbl_sales=Label(self.root, text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE, bg="#ffc107",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650,y=300,height=150, width=300)
        #===footer======
        lbl_footer=Label(self.root,text="IMS-inventory management system | Developed By Mungaihub\n for any technical issues contact 0745xxxxxx",  font=("times new roman",12),bg="#4d636d",fg="white") .pack(side=BOTTOM, fill=X)
#======================================================================
        self.update_date_time()
        self.update_content()

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeclass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierclass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryclass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productclass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesclass(self.new_win)

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")    
        self.lbl_clock.config(text=f"welcome to inventory management system\t\t Date: {str(date_)}\t\t Time:{str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total category\n[ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')

            self.lbl_sales.config(text=f'Total Sales [{str(len(os.listdir('bill')))}]')
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()