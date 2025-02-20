from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillingClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1370x700+0+0")
        self.root.title("inventory management system | developed by Amos")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        #====title=======
        self.icon_title=PhotoImage(file="images/cart1.png")
        title=Label(self.root,text="inventory management system", image=self.icon_title, compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white", anchor="w", padx=20).place(x=0,y=0, relwidth=1, height=70)
        

        #====btn_loogout===
        btn_logout=Button(self.root, text="Logout", command=self.logout,font=("times new roman", 15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        
        #===clock======
        self.lbl_clock=Label(self.root,text="welcome to inventory management system\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",  font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70, relwidth=1, height=30)

        #======product frame=======
        self.var_search=StringVar()
        productframe=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        productframe.place(x=6,y=110,width=410, height=550)

        producttitle=Label(productframe,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        productframe2=Frame(productframe,bd=4,relief=RIDGE,bg="white")
        productframe2.place(x=2,y=42,width=398, height=90)

        lblsearch=Label(productframe2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lblname=Label(productframe2,text="Product Name",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=2,y=45)
        txt_search=Entry(productframe2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btn_search=Button(productframe2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(productframe2,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        productframe3=Frame(productframe,bd=3,relief=RIDGE)
        productframe3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(productframe3,orient=VERTICAL)
        scrollx=Scrollbar(productframe3,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(productframe3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid", text="PID")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="QTY")
        self.ProductTable.heading("status", text="Status")
        
        self.ProductTable["show"]="headings"
        
        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        lblnote=Label(productframe,text="Note: 'Enter  0 Quantity to remove product from the cart'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #========customerframe===========
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        customerframe=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        customerframe.place(x=420,y=110,width=530,height=70)

        customertitle=Label(customerframe,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lblname=Label(customerframe,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(customerframe,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

        lblcontact=Label(customerframe,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(customerframe,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
        
        #====cal cart frame=======
        cal_cart_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cal_cart_frame.place(x=420,y=190,width=530,height=360)

        #====calculator frame=======
        self.var_cal_input=StringVar()

        cal_frame=Frame(cal_cart_frame,bd=9,relief=RIDGE,bg="white")
        cal_frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(cal_frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(cal_frame,text=7,font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
        btn_8=Button(cal_frame,text=8,font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
        btn_9=Button(cal_frame,text=9,font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
        btn_plus=Button(cal_frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3)
        
        btn_4=Button(cal_frame,text=4,font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
        btn_5=Button(cal_frame,text=5,font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
        btn_6=Button(cal_frame,text=6,font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
        btn_minus=Button(cal_frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3)
        
        btn_1=Button(cal_frame,text=1,font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=0)
        btn_2=Button(cal_frame,text=2,font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=1)
        btn_3=Button(cal_frame,text=3,font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=2)
        btn_mult=Button(cal_frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=3)
        
        btn_zero=Button(cal_frame,text=0,font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=0)
        btn_c=Button(cal_frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=1)
        btn_eq=Button(cal_frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=2)
        btn_div=Button(cal_frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=3)
        
        #====cart frame=======
        cartframe=Frame(cal_cart_frame,bd=3,relief=RIDGE)
        cartframe.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cartframe,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cartframe,orient=VERTICAL)
        scrollx=Scrollbar(cartframe,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cartframe,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
            
        self.CartTable["show"]="headings"
            
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #====add cart widgets frame==========
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        Add_cartwidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_cartwidgetsFrame.place(x=420,y=550,width=530,height=110)

        lblProductname=Label(Add_cartwidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txtProductname=Entry(Add_cartwidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lblProductPrice=Label(Add_cartwidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txtProductPrice=Entry(Add_cartwidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lblProductQty=Label(Add_cartwidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txtProductQty=Entry(Add_cartwidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(Add_cartwidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_cartwidgetsFrame,command=self.clear_cart,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_cartwidgetsFrame,command=self.add_update_cart,text="Add | Update Cart",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #=========billing area========
        billframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billframe.place(x=953,y=110,width=410,height=410)

        billingtitle=Label(billframe,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#FF8C00",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billframe,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.txt_bill_area=Text(billframe,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #============billing buttons============
        billmenuframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billmenuframe.place(x=953,y=520,width=410,height=140)

        self.lbl_amnt=Label(billmenuframe,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billmenuframe,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billmenuframe,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)


        btn_print=Button(billmenuframe,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear=Button(billmenuframe,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billmenuframe,text="Generate/Save Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

        #===footer======
        lbl_footer=Label(self.root,text="IMS-inventory management system | Developed By Mungaihub\n for any technical issues contact 0745xxxxxx",  font=("times new roman",12),bg="#4d636d",fg="white") .pack(side=BOTTOM, fill=X)

        self.show()
        #self.bill_top()
        self.update_date_time()

        #=========All Functions================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'") 
            
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")


                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror('Error',"Please select the product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
        
        
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
        
            #========update cart=======
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
        if present=='yes':
            op=messagebox.askyesno('Confirm',"Product already present\nDo you want to update| Remove from the cart list",parent=self.root)
            if op==True:
                if self.var_qty.get()=="0":
                    self.cart_list.pop(index_)
                else:
                    #self.cart_list[index_][2]=price_cal
                    self.cart_list[index_][3]=self.var_qty.get()
        
        
        else:
            self.cart_list.append(cart_data)
        
        self.show_cart()
        self.bill_updates()
    
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n[{str(self.net_pay)}]')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent= self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the cart!!!",parent= self.root)
        else:
            #======bill top====
            self.bill_top()
            #======bill middle====
            self.bill_middle()
            #======bill bottom====
            self.bill_bottom()
        
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/save in backend",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%H%M%S"))
        bill_top_temp=f'''
\t\tMungaiHub-Inventory
\t Phone No. 0745xxxxx, Nairobi-120056
{str("="*47)}
Customer Name: {self.var_cname.get()}
Phone No.: {self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tKsh.{self.bill_amnt}
Discount\t\t\t\tKsh.{self.discount}
Net Pay\t\t\t\tKsh.{self.net_pay}
{str("="*47)}
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:

            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tKsh."+price)

                #======update qty in product table===
                cur.execute('update product set qty=?,status=? where pid=?',(
                qty,
                status,
                pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)
    
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")    
        self.lbl_clock.config(text=f"welcome to inventory management system\t\t Date: {str(date_)}\t\t Time:{str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill,to print the receipt",parent=self.root)
           
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root=Tk()
    obj=BillingClass(root)
    root.mainloop()