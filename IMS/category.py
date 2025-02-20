from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
class categoryclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("inventory management system | developed by Amos")
        self.root.config(bg="white")
        self.root.focus_force()
        #########variables############
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #=========tittle=============
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=10)

        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="Add",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=130,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=510,y=170,width=130,height=30)

        #==========supplier details=========
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=670,y=100,width=400,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient="horizontal")

        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cat_id","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cat_id", text="Cat_id")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cat_id",width=90)
        self.CategoryTable.column("name",width=100) 
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)

        #======images=========
        self.im1=Image.open("images/category1.jpg")
        self.im1=self.im1.resize((500,250),Image.Resampling.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("images/category2.jpg")
        self.im2=self.im2.resize((500,250),Image.Resampling.LANCZOS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2)
        self.lbl_im2.place(x=580,y=220)

        self.show()
        #========functions=====
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","category already present, try diffirent",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(self.var_name.get(),))

                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category") 
            
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","please select category name from the list",parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cat_id=?", (self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error,please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cat_id=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)
            


if __name__ == "__main__":
    root=Tk()
    obj=categoryclass(root)
    root.mainloop()