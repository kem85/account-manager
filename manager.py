import os
import ttkbootstrap as tb
from tkinter import messagebox
from tkinter import BooleanVar, Toplevel, Frame, BOTH, LEFT, RIGHT, VERTICAL, Y
from ttkbootstrap.constants import PRIMARY
import sqlite3
conn = sqlite3.connect(f'{os.getcwd()}/accounts.db')
cun = conn.cursor()
options = []
cun.execute('''CREATE Table IF NOT EXISTS database (
    cata     TEXT,
    ID       TEXT,
    name     TEXT,
    email    TEXT,
    password TEXT,
    color    TEXT DEFAULT ('6e40c0') 
);''')
def update_combobox():
    cun.execute('''SELECT name FROM database WHERE cata == 'false' ''')
    options.clear()
    for i in cun:
        options.append(i)
update_combobox()
root = tb.Window(themename="vapor")
text_var = tb.StringVar()
name_var = tb.StringVar()
state_var = tb.StringVar(value='LLm')
canscroll_var = tb.BooleanVar(value=True)
email_var = tb.StringVar()
color_var = tb.StringVar()
id_var = tb.StringVar()
posbut_var =tb.IntVar()
password_var = tb.StringVar()
catagory_var = tb.IntVar()
buttons= tb.Style()
search_name = []
buttonss = []
buttons2 = []
button_id = {}
buttons.configure('Custom.TButton', font=('Helvetica', 12),foreground='#C0C0C0')
def on_text_change(*args): #search
    global search_name,buttonss
    if state_var.get()=='LLm':
        cun.execute('''SELECT name FROM database WHERE cata == 'false' ''')
    else:
        cun.execute('''SELECT name FROM database WHERE cata = ?''',(state_var.get(),))
    templst = cun.fetchall()
    lst = []
    for i in range(len(templst)):
        lst.append(templst[i][0])
    curt = text_var.get()
    nlst = [word[:-(len(word)-len(curt))] if len(word) > len(curt) else word for word in lst] #lst is the names
    for i,cur in enumerate(nlst):
        if cur == curt and len(curt)!=0:
            search_name.append(lst[i])
    if state_var.get()=='LLm':
        windowcreate('searchc')
    else:
        windowcreate('searchb')
    search_name.clear()
    if(text_var.get() == ""):
        if state_var.get()=='LLm':
            windowcreate('catagory')
        else:
            windowcreate(state_var.get())
def on_mousewheel(event): #scrolling
    if canscroll_var.get():
         my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def update_scrollregion(count = 0): #update 4 scrolling
    if count <= 0:
        count = readbase('countc')
    min_height = 500  
    my_canvas.update_idletasks()
    bbox = my_canvas.bbox("all")
    my_canvas.configure(scrollregion=(bbox[0], bbox[1], bbox[2], max(bbox[3], min_height)))
    second_frame.update_idletasks()
    second_frame.configure(width=340, height=count*35) #50*45, 45 is y for each button and 50 is number of button
def ADD(): #this will make it to THAT window
    def clear(cond):
        if catagory_var.get() == 1:
            cun.execute('''SELECT name FROM database WHERE cata == 'false' ''')
        else:
            cun.execute('''SELECT name FROM database WHERE cata = ? ''',(Combo_Box.get(),))
        namer = cun.fetchall()
        filter=False
        for i in range(len(namer)):
            if name_var.get() in namer[i]:
                filter = True
        if cond == 0:
            if not filter and ((len(color_var.get()) == 6) or color_var.get() == "") and name_var.get() != "" and ((email_var.get() != "" and password_var.get() !="" and Combo_Box.get() != "") or catagory_var.get()):
                Submit.configure(state = 'disabled')
                messagebox.showinfo(title="Successful", message="Added account successfully")
                Submit.configure(state = 'enabled')
                if readbase("countc") != 0 and catagory_var.get():
                    id_var.set(f"{readbase("countc")+1}")
                elif catagory_var.get():
                    id_var.set("1")
                else:
                    count = 1
                    cun.execute("SELECT ID FROM database WHERE name = ?", (Combo_Box.get(),))
                    ID = cun.fetchone()[0]
                    cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2")
                    for i in cun:
                        if i[0][0] == ID:
                            count += 1
                    id_var.set(f"{ID}/{count}")
                database(name_var.get(),email_var.get(),password_var.get(),color_var.get() or "6e40c0",Combo_Box.get() or "false",id_var.get())
                update_combobox()
                Combo_Box.configure(values=options)
                windowcreate('catagory',True)
            else:
                Submit.configure(state = 'disabled')
                messagebox.showerror("Unsuccessful", "Invaild Format") 
                Submit.configure(state = 'enabled')
            name_var.set("")
            color_var.set("")
            email_var.set("")
            password_var.set("")
        elif cond==1 and catagory_var.get() == 1:
            Combo_Box.set("")
            Email_Label.grid_remove()
            Email_Entry.grid_remove()
            Password_Label.grid_remove()
            Password_Entry.grid_remove()
            Combo_Box.place_forget()
        elif cond == 1 and catagory_var.get() == 0:
            Email_Label.grid()
            Email_Entry.grid()
            Password_Label.grid()
            Password_Entry.grid()
            Combo_Box.place(x=269,y=260)
    global addwindow,editwindow,buttonwindow
    if not addwindow.get() and not editwindow.get():
        addwindow.set(True)
        canscroll_var.set(False)
        addacc = Toplevel(root)
        addacc.title("Add Account")
        deffont = ('Helvetica', 18)
        windowWidth = 425
        windowHeight = 300
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        centerX = int(screenWidth/2 - windowWidth / 2)
        centerY = int(screenHeight/2 - windowHeight / 2)
        addacc.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
        addacc.resizable(False, False)
        addacc.protocol("WM_DELETE_WINDOW", lambda: (addwindow.set(False) , addacc.destroy(),canscroll_var.set(True)))
        Name_Label = tb.Label(addacc, text='Name:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
        Name_Label.grid(column=0,row=0)
        Email_Label = tb.Label(addacc, text='Email:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
        Email_Label.grid(column=0,row=1)
        Password_Label = tb.Label(addacc, text='Pass:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
        Password_Label.grid(column=0,row=2)
        Color_Label = tb.Label(addacc, text='Color:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
        Color_Label.grid(column=0,row=3)
        Name_Entry = tb.Entry(addacc,width=15,textvariable=name_var,font=deffont)
        Email_Entry = tb.Entry(addacc,width=15,font=deffont,textvariable=email_var)
        Password_Entry = tb.Entry(addacc,width=15,font=deffont,textvariable=password_var)
        Color_Entry = tb.Entry(addacc,width=15,font=deffont,textvariable=color_var)
        Name_Entry.grid(column=1,row=0,pady=10,padx=5)
        Email_Entry.grid(column=1,row=1,pady=10,padx=5)
        Password_Entry.grid(column=1,row=2,pady=10,padx=5)
        Color_Entry.grid(column=1,row=3,pady=10,padx=5)
        addacc.option_add('*TCombobox*Listbox.font', ('Helvetica', 14))
        Combo_Box = tb.Combobox(addacc,values=options,font=('Helvetica', 14),width=10)
        style = tb.Style()
        style.configure('Custom.TCheckbutton', font=('Helvetica', 18),foreground='#C0C0C0')
        Catagory = tb.Checkbutton(addacc,width=10,text="Catagory",onvalue=1,offvalue=0,style='Custom.TCheckbutton',variable=catagory_var,command=lambda:clear(1))
        Submit = tb.Button(addacc,takefocus=False,width=10,style='Custom.TButton',text="Submit",command=lambda:(clear(0)))
        Catagory.place(x=10,y=260)
        Combo_Box.place(x=269,y=260)
        Submit.place(x=135,y=260)
def EDIT(): #same thing
    global editwindow,addwindow,buttonwindow
    if not editwindow.get() and not addwindow.get():
        editwindow.set(True)
        canscroll_var.set(False)
        editacc = Toplevel(root)
        windowWidth = 450
        windowHeight = 300
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        centerX = int(screenWidth/2 - windowWidth / 2)
        centerY = int(screenHeight/2 - windowHeight / 2)
        editacc.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
        editacc.resizable(False, False)
        editacc.protocol("WM_DELETE_WINDOW", lambda: (editwindow.set(False) , editacc.destroy(),canscroll_var.set(True)))
def database(name,email,password,color, catagory,id):
    sql = ''' INSERT INTO database(name,email,password,color,cata,ID)
              VALUES(?,?,?,?,?,?) '''
    comm = [(name, email, password,color,catagory,id),]
    cun.executemany(sql, comm)
    conn.commit()
def readbase(indic,id = 0):
    count = 0
    if indic == "countc":
        cun.execute('''
                    SELECT COUNT(cata) FROM database WHERE cata == 'false'
                    ''')
        return cun.fetchone()[0]
    elif indic == "countb":
        cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2")
        for i in cun:
            if i[0][0] == id:
                count += 1
        return count
def windowcreate(indic,update = False): #this will make it THAT window
    global poscat_var,posbut_var,buttonss,state_var
    if indic == 'catagory':
            if update:
                for button in buttonss:
                    button.place_forget()
            buttonss.clear()
            cun.execute("SELECT name FROM database WHERE cata = 'false'")
            names = cun.fetchall()
            for i in range(readbase('countc')): #45 buttons
                button = tb.Button(second_frame, text=f'{names[i][0]}',takefocus=False,width=13,style='Custom.TButton')
                button.configure(command=lambda b = names[i][0]: windowcreate(b))
                if i % 2 == 0:
                    button.place(x=8, y = i*35)
                else:
                    button.place(x=179, y=(i-1)*35)
                buttonss.append(button)
            update_scrollregion()
    elif indic == 'searchc':
        global search_name
        for button in buttonss:
                 button.place_forget()
        buttonss.clear()
        for i in range(len(search_name)):
            button = tb.Button(second_frame, text=f'{search_name[i]}',takefocus=False,width=13,style='Custom.TButton')
            button.configure(command=lambda b = search_name[i]: windowcreate(b))
            if i % 2 == 0:
                button.place(x=8, y = i*35)
            else:
                button.place(x=179, y=(i-1)*35)
            buttonss.append(button)
        update_scrollregion(len(search_name))
    elif indic == 'searchb':
        for button in buttons2:
             button.place_forget()
        buttons2.clear()
        for i in range(len(search_name)):
            button = tb.Button(second_frame, text=f'{search_name[i]}',takefocus=False,width=10,style='Custom.TButton')
            if i % 2 == 0:
                button.place(x=8, y = i*35)
            else:
                button.place(x=179, y=(i-1)*35)
            buttons2.append(button)
        update_scrollregion(len(search_name))
    else:
            global my_canvas
            if state_var.get() == 'LLm':
                for widget in second_frame.winfo_children():
                    widget.place_forget()
                windowWidth = 325
                windowHeight = 450
                screenWidth = root.winfo_screenwidth()
                screenHeight = root.winfo_screenheight()
                centerX = int(screenWidth/2 - windowWidth / 2)
                centerY = int(screenHeight/2 - windowHeight / 2)
                root.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
            state_var.set(indic)
            cun.execute("SELECT ID FROM database WHERE name = ?", (indic,))
            id = cun.fetchone()[0]
            # subcata.resizable(False, False)
            second_frame.configure(width=325, height=readbase('countb',id) * 35) #50*45, 45 is y for each button and 50 is number of button
            my_canvas.configure(width = 100, height = 150)
            cun.execute("SELECT name FROM database WHERE LENGTH(ID) > 2 AND cata = ?",(indic,))
            tempname = cun.fetchall()
            subnames = []
            for i in range(len(tempname)):
                subnames.append(tempname[i][0])
            for i in range(readbase('countb',id)):
                button = tb.Button(second_frame, text=f'{subnames[i]}',takefocus=False,width=10,style='Custom.TButton')
                if i % 2 == 0:
                    button.place(x=8, y = i*35)
                else:
                    button.place(x=179, y=(i-1)*35)
                buttons2.append(button)
            update_scrollregion(len(tempname))
            

addwindow = BooleanVar()
editwindow = BooleanVar()
#buttonwindow = BooleanVar()
#####################################################################
def default_page():
    global my_canvas,second_frame
    root.title("Accounts")
    windowWidth = 335
    windowHeight = 450
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    centerX = int(screenWidth/2 - windowWidth / 2)
    centerY = int(screenHeight/2 - windowHeight / 2)
    root.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    # root.resizable(False, False)
    #####################################################################
    main_frame = tb.Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = tb.Canvas(main_frame, width=100, height=405)
    root.configure(bg='#110833')
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_scrollbar = tb.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    second_frame = Frame(my_canvas, width=340, height=readbase('countc')*35) #50*45, 45 is y for each button and 50 is number of button
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    search = tb.Entry(root, textvariable=text_var,width=30)
    edit = tb.Button(root, text='Edit',takefocus=False,width=5,style=PRIMARY,command=lambda:EDIT())
    edit.pack(side='right', anchor='e')
    search.pack(side='right', anchor='w',expand=True,padx=15,pady=5)
    add = tb.Button(root, text='Add',takefocus=False,width=5,style=PRIMARY,command=lambda:ADD())
    add.pack(side='left', anchor='e')
    # Update scroll region to include all buttons
    windowcreate('catagory')
    update_scrollregion()
    my_canvas.bind_all("<MouseWheel>", on_mousewheel)  
default_page()
# Bind mouse wheel scrolling
text_var.trace_add("write", on_text_change)
root.mainloop()
