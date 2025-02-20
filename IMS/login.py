from tkinter import*
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import os
import email_pass
import smtplib
import random 

class login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("login system")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''

        #======images============
        self.login_image=ImageTk.PhotoImage(file="images/login2.jpg")
        self.lbl_login_image=Label(self.root,image=self.login_image,bd=0,).place(x=150,y=50)

        #====login frame========
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=750,y=150,width=350,height=460)

        title=Label(login_frame,text="Login system",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)
      
        lbl_user=Label(login_frame,text="Employee ID",font=("andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_empid=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

         
        lbl_pass=Label(login_frame,text="Password",font=("andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,font=("times new roman",15),bg="#ECECEC",show="*").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00b0f0",activebackground="#00b0f0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("time new roman",15)).place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",activebackground="white",activeforeground="#00759E",bd=0,cursor="hand2").place(x=100,y=390)

        

    def login(self):

        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("select * from employee where empid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
            if user==None:
                messagebox.showerror('Error',"Invalid Username/Password",parent=self.root)
            else:
                if user[8]=="Admin":
                    self.root.destroy()
                    os.system("python dashboard.py")
                else:
                    self.root.destroy()
                    os.system("python billing.py")
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee Id must be required",parent=self.root)
            else:
                cur.execute("select email from employee where empid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee Id, try again",parent=self.root)
                else:
                    #======forget window===========
                    self.var_otp=StringVar()
                    self.var_new_password=StringVar()
                    self.var_conf_password=StringVar()
                    #call send_email_function()
                    chk=self.send_email(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:

                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus()

                        title=Label(self.forget_win,text='Reset Password',font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        
                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win,text="SUBMIT",font=("times new roman",15),bg="lightblue",cursor="hand2")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_password,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        conf_pass=Label(self.forget_win,text="Confirmed Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_password,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",state=DISABLED,font=("times new roman",15),bg="lightblue",cursor="hand2")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
                    



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent= self.root)

    def send_email(self, to_):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            email_='njamaa91@gmail.com'
            pass_='gyly vaer udaa cwno'

            s.login(email_, pass_)

            self.otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP

            subj = 'IMS-Reset Password OTP'
            msg = f'Dear Sir/Madam,\n\nYour reset OTP is {str(self.otp)}.\n\nWith regards,\nIMS Team'
            msg = f"Subject: {subj}\n\n{msg}"
            
            s.sendmail(email_, to_, msg)
            chk = s.ehlo()
            s.quit()

            if chk[0] == 250:
                return 's'
            else:
                return 'f'
        except Exception as e:
            return f'Error: {str(e)}'




root=Tk()
obj=login_system(root)
root.mainloop()