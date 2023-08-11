
                            #---Mohd Sadik---

                            
from tkinter import *
from tkinter import messagebox,filedialog
from tkinter.scrolledtext import ScrolledText
import time
import re
from PIL import Image,ImageTk
import os
import shutil
import sqlite3

try:
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("create table txn(acn int,type text,amt float,updatedbal float,date text)")
    con.commit()
    con.close()
    print("table created")
except:
    print("something went wrong,might be table already exists")

try:
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("create table accounts(acn integer primary key autoincrement,name text,pass text,mob text,email text,bal float,date text)")
    con.commit()
    con.close()
    print("table created")
except:
    print("something went wrong,might be table already exists")

win=Tk()
win.state("zoomed")
win.configure(bg="powder blue")

title=Label(win,text="Banking Simulation",font=('arial',50,'bold','underline'),bg='powder blue').pack()

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

font_tup=('arial',20,'bold')
frm_bgclr='pink'

def login_screen():
    frm=Frame(win)
    frm.configure(bg=frm_bgclr)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def reset():
        entryacn.delete(0,"end")
        entrypass.delete(0,"end")
        entryacn.focus()
    
    def login():
        acn=entryacn.get()
        pwd=entrypass.get()
        if(len(acn)==0 or len(pwd)==0):
            messagebox.showwarning("Validation","Fields can't be empty")
            return
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select * from accounts where acn=? and pass=?",(acn,pwd))
        global tup
        tup=cur.fetchone()
        if(tup==None):
            messagebox.showerror("Login","Invalid ACN/PASS")
            return
        else:
            frm.destroy()
            welcome_screen() 
    
    def opennew():
        frm.destroy()
        newuser_screen()
    
    def forgot():
        frm.destroy()
        forgot_screen()
    
    lblacn=Label(frm,text="Account No",font=font_tup,bg=frm_bgclr)
    lblacn.place(relx=.3,rely=.15)

    entryacn=Entry(frm,font=font_tup,bd=5)
    entryacn.place(relx=.45,rely=.15)
    entryacn.focus()
    
    lblpass=Label(frm,text="Password",font=font_tup,bg=frm_bgclr)
    lblpass.place(relx=.3,rely=.25)

    entrypass=Entry(frm,font=font_tup,bd=5,show='*')
    entrypass.place(relx=.45,rely=.25)
    
    
    loginbtn=Button(frm,text="login",font=font_tup,bd=5,command=login)
    loginbtn.place(relx=.4,rely=.4)
    
    resetbtn=Button(frm,text="reset",font=font_tup,bd=5,command=reset)
    resetbtn.place(relx=.5,rely=.4)
    
    newuserbtn=Button(frm,text="open new account",font=font_tup,bd=5,width=20,command=opennew)
    newuserbtn.place(relx=.38,rely=.55)
    
    fpbtn=Button(frm,text="forgot password",font=font_tup,bd=5,width=27,command=forgot)
    fpbtn.place(relx=.35,rely=.7)
 

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg=frm_bgclr)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    lbl=Label(frm,text="Open New Account",font=font_tup,bg=frm_bgclr,fg='blue')
    lbl.pack()
    
    def back():
        frm.destroy()
        login_screen()
    
    def reset():
        entryname.delete(0,"end")
        entrypass.delete(0,"end")
        entrymob.delete(0,"end")
        entrymail.delete(0,"end")
        entryname.focus()
    
    def register():
        name=entryname.get()
        pwd=entrypass.get()
        mob=entrymob.get()
        email=entrymail.get()
        r=re.fullmatch('[6-9][0-9]{9}',mob)
        if(len(name)==0 or len(pwd)==0 or len(mob)==0 or len(email)==0):
                    messagebox.showwarning("Validation","Fields Cannot be Empty")
                    return
        if r==None: 
                    messagebox.showwarning("Validation","Invalid Number")
                    return
        if email_regex.match(email) == None:
                    messagebox.showwarning("Validation","Invalid Email")
                    return
        bal=0.0
        date=time.ctime()
        import sqlite3
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(name,pass,mob,email,bal,date) values(?,?,?,?,?,?)",(name,pwd,mob,email,bal,date))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(acn) from accounts")
        tup=cur.fetchone()
        con.commit()
        
        messagebox.showinfo("Success",f"Account opened with Account No:{tup[0]}")
        frm.destroy()
        login_screen()
    backbtn=Button(frm,text="back",font=font_tup,bd=5,command=back)
    backbtn.place(relx=0,rely=0)
    
    
    lblname=Label(frm,text="Name",font=font_tup,bg=frm_bgclr)
    lblname.place(relx=.3,rely=.15)

    entryname=Entry(frm,font=font_tup,bd=5)
    entryname.place(relx=.45,rely=.15)
    entryname.focus()
    
    lblpass=Label(frm,text="Password",font=font_tup,bg=frm_bgclr)
    lblpass.place(relx=.3,rely=.25)

    entrypass=Entry(frm,font=font_tup,bd=5,show='*')
    entrypass.place(relx=.45,rely=.25)
    
    
    lblmob=Label(frm,text="Mob",font=font_tup,bg=frm_bgclr)
    lblmob.place(relx=.3,rely=.35)

    entrymob=Entry(frm,font=font_tup,bd=5)
    entrymob.place(relx=.45,rely=.35)
    
    lblmail=Label(frm,text="Email",font=font_tup,bg=frm_bgclr)
    lblmail.place(relx=.3,rely=.45)

    entrymail=Entry(frm,font=font_tup,bd=5)
    entrymail.place(relx=.45,rely=.45)
    
    regbtn=Button(frm,text="register",font=font_tup,bd=5,command=register)
    regbtn.place(relx=.4,rely=.6)
    
    resetbtn=Button(frm,text="reset",font=font_tup,bd=5,command=reset)
    resetbtn.place(relx=.5,rely=.6)
 

def forgot_screen():
    frm=Frame(win)
    frm.configure(bg=frm_bgclr)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    lbl=Label(frm,text="Recover your password",font=font_tup,bg=frm_bgclr,fg='blue')
    lbl.pack()
    
    def back():
        frm.destroy()
        login_screen()

    def reset():
        entryacn.delete(0,"end")
        entrymob.delete(0,"end")
        entrymail.delete(0,"end")
        entryacn.focus()
        
    
    def recover():
        acn=entryacn.get()
        mob=entrymob.get()
        email=entrymail.get()
        r=re.fullmatch('[6-9][0-9]{9}',mob)
        if(len(acn)==0 or len(mob)==0 or len(email)==0):
            messagebox.showwarning("Validation","Fields can't be empty")
            return
        if r==None: 
                  messagebox.showwarning("Validation","Invalid Number")
                  return
        if email_regex.match(email) == None:
                   messagebox.showwarning("Validation","Invalid Email")
                   return
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select pass from accounts where acn=? and mob=? and email=?",(acn,mob,email))
        tup_pass=cur.fetchone()
        if(tup_pass==None):
            messagebox.showerror("Recover","Account does not exist not given details")
        else:
            messagebox.showinfo("Recover",f"Your Password :{tup_pass[0]}")
            frm.destroy()
            login_screen()
    backbtn=Button(frm,text="back",font=font_tup,bd=5,command=back)
    backbtn.place(relx=0,rely=0)
    
    
    lblacn=Label(frm,text="Account No",font=font_tup,bg=frm_bgclr)
    lblacn.place(relx=.3,rely=.25)

    entryacn=Entry(frm,font=font_tup,bd=5)
    entryacn.place(relx=.45,rely=.25)
    entryacn.focus()
    

    lblmob=Label(frm,text="Mob",font=font_tup,bg=frm_bgclr)
    lblmob.place(relx=.3,rely=.35)

    entrymob=Entry(frm,font=font_tup,bd=5)
    entrymob.place(relx=.45,rely=.35)
    
    lblmail=Label(frm,text="Email",font=font_tup,bg=frm_bgclr)
    lblmail.place(relx=.3,rely=.45)

    entrymail=Entry(frm,font=font_tup,bd=5)
    entrymail.place(relx=.45,rely=.45)
    
    recoverbtn=Button(frm,text="recover",font=font_tup,bd=5,command=recover)
    recoverbtn.place(relx=.4,rely=.6)
    
    resetbtn=Button(frm,text="reset",font=font_tup,bd=5,command=reset)
    resetbtn.place(relx=.5,rely=.6)
 

def welcome_screen():
    frm=Frame(win)
    frm.configure(bg=frm_bgclr)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    if(os.path.exists(f"pics/{tup[0]}.jpg")):
        path=f"pics/{tup[0]}.jpg"
    else:
        path="pics/default_pic.jpg"
    
    img=Image.open(path)
    img=img.resize((150,120))
    imgtk=ImageTk.PhotoImage(img,master=win)
    
    lblpic=Label(frm,image=imgtk)
    lblpic.place(relx=.005,rely=.005)
    lblpic.image=imgtk
    
    def set():
        imgpath=filedialog.askopenfilename()
        newpicname=f"pics/{tup[0]}.jpg"
        if(os.path.exists(newpicname)):
            os.remove(newpicname)
        shutil.copy(imgpath,newpicname)
        img=Image.open(newpicname)
        img=img.resize((150,120))
        imgtk=ImageTk.PhotoImage(img,master=win)
        lblpic=Label(frm,image=imgtk)
        lblpic.place(relx=.005,rely=.005)
        lblpic.image=imgtk
        
    setbtn=Button(frm,text='set',command=set)
    setbtn.place(relx=.14,rely=.18)
    
    def logout():
        frm.destroy()
        login_screen()
    
    
    def withdraw_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        bg='white'
        ifrm.configure(bg=bg)
        ifrm.place(relx=.2,rely=.15,relwidth=.6,relheight=.7)
        lbl=Label(ifrm,text="Withdraw Operation",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.pack()
    
        def withdrawamt():
            amt=float(entyamt.get())
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from accounts where acn=?",(tup[0],))
            updatebal=cur.fetchone()[0]
            con.close()
            if(updatebal>=amt and amt>0):          
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(tup[0],'Dr',amt,updatebal,time.ctime()))
                cur.execute("update accounts set bal=bal-? where acn=?",(amt,tup[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Withdraw","Amount succefully withdraw ")
            else:
                 messagebox.showwarning("Alert","Entered amount is greater than current balance or zero")
    
        lblamt=Label(ifrm,text="Enter Amount:",font=('arial',15,'bold'),bg='white',fg='red')
        lblamt.place(relx=.2,rely=.2)
        
        entyamt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entyamt.place(relx=.45,rely=.2)
        
        btn=Button(ifrm,text="submit",font=('arial',15,'bold'),bd=5,command=withdrawamt)
        btn.place(relx=.35,rely=.35)
    
    
    def deposit_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        bg='white'
        ifrm.configure(bg=bg)
        ifrm.place(relx=.2,rely=.15,relwidth=.6,relheight=.7)
        lbl=Label(ifrm,text="Deposit Operation",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.pack()
    
        def depositamt():
            amt=float(entyamt.get())
            if(amt>0):
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select bal from accounts where acn=?",(tup[0],))
                updatebal=cur.fetchone()[0]
                con.close()
                        
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(tup[0],'Cr',amt,updatebal,time.ctime()))
                cur.execute("update accounts set bal=bal+? where acn=?",(amt,tup[0]))
                con.commit()
                con.close()
            
                messagebox.showinfo("Deposit","Amount deposited")
            else:
                messagebox.showerror("Failed","Please deposit amount greater than 0")
            
        lblamt=Label(ifrm,text="Enter Amount:",font=('arial',15,'bold'),bg='white',fg='red')
        lblamt.place(relx=.2,rely=.2)
        
        entyamt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entyamt.place(relx=.45,rely=.2)
        
        btn=Button(ifrm,text="submit",font=('arial',15,'bold'),bd=5,command=depositamt)
        btn.place(relx=.35,rely=.35)
    
    
    def bal_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        bg='white'
        ifrm.configure(bg=bg)
        ifrm.place(relx=.2,rely=.15,relwidth=.6,relheight=.7)
        lbl=Label(ifrm,text="Your Account Details",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.pack()
    
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select bal from accounts where acn=?",(tup[0],))
        bal=cur.fetchone()[0]
        con.close()
        lbl_details=Label(ifrm,text=f"Account No:{tup[0]}\n\nAvailable Bal:{bal}",font=('',20,'bold'),bg=bg,fg='blue')
        lbl_details.place(relx=.3,rely=.3)
        
    def txn_history():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        
        myscrollbar=Scrollbar(ifrm,orient="vertical")
        myscrollbar.pack(side="right",fill="y")
        
        bg='white'
        ifrm.configure(bg=bg)
        ifrm.place(relx=.2,rely=.15,relwidth=.6,relheight=.7)
        
        lbl=Label(ifrm,text="Your transaction Histroy",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.pack()
        
        lbl=Label(ifrm,text="Type\t\t\tAmount\t\t\tDate",font=('',20,'bold'),bg=bg,fg='red')
        #lbl.place(relx=.15,rely=.12)
        
        st=ScrolledText(ifrm,width=80,height=15)
        st.place(relx=.05,rely=.12)
        st.delete('1.0',END)
        
        msg="Type\tAmount\t\tDate\t\t\t\tUpdated bal\n\n"
        
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select type,amt,date,updatedbal from txn where acn=?",(tup[0],))
        tr=reversed(cur.fetchall())
        for tp in tr:
            msg=msg+f" {tp[0]}\t{tp[1]}\t\t{tp[2]}\t\t\t\t{tp[3]}\n\n"
        con.close()
        st.insert(END,msg)
    def update_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        bg='white'
        ifrm.configure(bg=bg)
        ifrm.place(relx=.2,rely=.15,relwidth=.6,relheight=.7)
        lbl=Label(ifrm,text="Update Your Details",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.pack()
        
        def upd_details():
            name=entryname.get()
            pwd=entrypass.get()
            mob=entrymob.get()
            email=entrymail.get()
            r=re.fullmatch('[6-9][0-9]{9}',mob)
            if(len(name)==0 or len(pwd)==0 or len(mob)==0 or len(email)==0):
                    messagebox.showwarning("Validation","Fields Cannot be Empty")
                    return
            if r==None: 
                    messagebox.showwarning("Validation","Invalid Number")
                    return
            if email_regex.match(email) == None:
                    messagebox.showwarning("Validation","Invalid Email")
                    return
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set name=?, pass=?, mob=?, email=? where acn=?",(name,pwd,mob,email,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("UPDATED","Details updated successfully")
    
        lblname=Label(ifrm,text="Name",font=font_tup,bg=bg)
        lblname.place(relx=.2,rely=.15)

        entryname=Entry(ifrm,font=font_tup,bd=5)
        entryname.place(relx=.35,rely=.15)
        entryname.focus()
        entryname.insert(0,tup[1])
    
        lblpass=Label(ifrm,text="Pass",font=font_tup,bg=bg)
        lblpass.place(relx=.2,rely=.3)

        entrypass=Entry(ifrm,font=font_tup,bd=5,show='*')
        entrypass.place(relx=.35,rely=.3)
        entrypass.insert(0,tup[2])
    
        lblmob=Label(ifrm,text="Mob",font=font_tup,bg=bg)
        lblmob.place(relx=.2,rely=.45)

        entrymob=Entry(ifrm,font=font_tup,bd=5)
        entrymob.place(relx=.35,rely=.45)
        entrymob.insert(0,tup[3])
        
        lblmail=Label(ifrm,text="Email",font=font_tup,bg=bg)
        lblmail.place(relx=.2,rely=.6)

        entrymail=Entry(ifrm,font=font_tup,bd=5)
        entrymail.place(relx=.35,rely=.6)
        entrymail.insert(0,tup[4])
        
        
        btn=Button(ifrm,text="submit",font=('arial',15,'bold'),bd=5,command=upd_details)
        btn.place(relx=.35,rely=.75)
    
    
    lbl=Label(frm,text=f"Welcome,{tup[1]}",font=font_tup,bg=frm_bgclr,fg='blue')
    lbl.pack()
    
    logoutbtn=Button(frm,text="logout",font=font_tup,bd=5,command=logout)
    logoutbtn.place(relx=.9,rely=0)
    
    
    withbtn=Button(frm,text="withdraw",font=font_tup,bd=5,width=12,command=withdraw_screen)
    withbtn.place(relx=0,rely=.25)
    
    updatebtn=Button(frm,text="update",font=font_tup,bd=5,width=12,command=update_screen)
    updatebtn.place(relx=0,rely=.4)
    
    balbtn=Button(frm,text="balance",font=font_tup,bd=5,width=12,command=bal_screen)
    balbtn.place(relx=0,rely=.55)
    
    txnbtn=Button(frm,text="txn history",font=font_tup,bd=5,width=12,command=txn_history)
    txnbtn.place(relx=0,rely=.7)
    
    depbtn=Button(frm,text="deposit",font=font_tup,bd=5,width=12,command=deposit_screen)
    depbtn.place(relx=0,rely=.85)
    
login_screen()
win.mainloop()



