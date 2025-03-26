import os
import ttkbootstrap as tb
import pyperclip
from tkinter import messagebox,BooleanVar, Toplevel, Frame, BOTH, LEFT, RIGHT, VERTICAL, Y
from ttkbootstrap.constants import PRIMARY
from ttkbootstrap.style import Style
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from PIL import Image, ImageTk 
import sqlite3
conn = sqlite3.connect(f'{os.getcwd()}/accounts.db')
cun = conn.cursor()
cun.execute('''CREATE Table IF NOT EXISTS database (
    cata     TEXT,
    ID       TEXT,
    name     TEXT,
    email    TEXT,
    password TEXT,
    color    TEXT DEFAULT ('6e40c0') 
);''')
root = tb.Window(themename="vapor")
text_var = tb.StringVar()
name_var = tb.StringVar()
state_bool = tb.BooleanVar(value="0")
state_var = tb.StringVar(value='LLm')
canscroll_var = tb.BooleanVar(value=True)
currentmenu_var = tb.StringVar()
email_var = tb.StringVar()
color_var = tb.StringVar()
id_var = tb.StringVar()
password_var = tb.StringVar()
widget_info = []
subcata_info= []
buttons= tb.Style()
search_name = []
cata_button = []
lst = []
buttons2 = []
buttons.configure('Custom.TButton', font=('Helvetica', 12),foreground='#C0C0C0')
def center(x,y):
    rs = []
    rs.append(x)
    rs.append(y)
    rs.append(int(root.winfo_screenwidth()/2 - x/ 2))
    rs.append(int(root.winfo_screenheight()/2 - y/2))
    return rs
def state_change(*args):
    global lst
    lst.clear()
    if add.cget("text")=="Back" and state_var.get() == "LLm":
        state_bool.set(0)
    else:
        state_bool.set(1)
def colorpicking(this):
    this.focus_force()
    cd = ColorChooserDialog(root)
    cd.show()
    if cd.result:
        color_var.set(cd.result[2][1:])
    this.after(100, lambda: this.focus_force())
    print(color_var.get())
def on_text_change(*args): # <=== this needs to be optimized
    global search_name,cata_button,lst
    curt = text_var.get()
    search_name.clear()
    if len(curt) != 0:
        if state_bool.get():
            cun.execute('''SELECT name FROM database WHERE (name LIKE ?) AND CATA = ?''', (f"%{curt}%", state_var.get()))
            results = cun.fetchall() 
            search_name.extend([result[0] for result in results])
        else:
            cun.execute("SELECT name, email FROM database WHERE cata = 'false' AND password = '' AND ((LENGTH(email) <= 0 AND name LIKE ?) OR (LENGTH(email) > 0 AND email LIKE ?))", (f"%{curt}%", f"%{curt}%"))
            results = cun.fetchall()
            search_name.extend([result[0] for result in results])
    if not state_bool.get():
        windowcreate.searchc()
    else:
        windowcreate.searchb()
    search_name.clear()
    if(text_var.get() == ""):
        if not state_bool.get():
            windowcreate.catagory()
        else:
            windowcreate.subcatagory(state_var.get())
def on_mousewheel(event): #scrolling
    if canscroll_var.get():
         my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def update_scrollregion(count = 0,update = False): #update 4 scrolling
    if count <= 0:            
        count = readbase.countc()
        if (count % 2 == 0) and update:
            count += 1
    min_height = 500
    bbox = my_canvas.bbox("all")
    my_canvas.configure(scrollregion=(bbox[0], bbox[1], bbox[2], max(bbox[3], min_height)))
    my_canvas.update_idletasks()
    second_frame.update_idletasks()
    my_canvas.yview_moveto(0)
    second_frame.configure(width=340, height=count*35) 
class ADD():
    global addwindow,editwindow,widget_info
    def submit(edit = False):
        global Submit, addacc
        if not state_bool.get():
            cun.execute('''SELECT name FROM database WHERE cata == 'false' AND password = '' ''')
        else:
            cun.execute('''SELECT name FROM database WHERE cata = ? ''',(state_var.get(),))
        namer = cun.fetchall()
        filter=False
        for i in range(len(namer)):
            if ( name_var.get() in namer[i] ) and not (name_var.get() == edit[2]):
                filter = True
        if not filter and ((len(color_var.get()) == 6) or color_var.get() == "") and name_var.get() != "" and ((email_var.get() != "" and password_var.get() !="" and state_bool.get()) or not state_bool.get()):
            global lst
            Submit.configure(state = 'disabled')
            text_var.set("")
            lst.append(name_var.get())
            messagebox.showinfo(title="Successful", message=f'{"Added" if not edit else "Edited"} {"Account" if state_bool.get() else "Catagory"} successfully')
            Submit.configure(state = 'enabled')
            addacc.focus_force()
            if not edit:
                if readbase.countc() != 0 and not state_bool.get():
                    id_var.set(f"{readbase.countc()+1}")
                elif not state_bool.get():
                    id_var.set("1")
                else:
                    count = 1
                    cun.execute("SELECT ID FROM database WHERE name = ?", (state_var.get(),))
                    ID = cun.fetchone()[0]
                    cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2")
                    for i in cun:
                        if i[0][0] == ID:
                            count += 1
                    id_var.set(f"{ID}/{count}")
                database(name_var.get(),email_var.get(),password_var.get(),color_var.get() or "6e40c0","false" if not state_bool.get() else state_var.get(),id_var.get())
            else:
                
                if state_bool.get():
                    cun.execute('''UPDATE database SET name = ?, email = ?, password = ?,color = ? WHERE cata = ? AND name = ?''',(name_var.get(), email_var.get(), password_var.get(),color_var.get() if color_var.get() else "6e40c0" ,state_var.get(), edit[2]))
                else:
                    cun.execute("UPDATE database SET email = ? WHERE cata = 'false' AND name = ?",(name_var.get(),edit[2],))
            conn.commit()

            if not state_bool.get():
                windowcreate.catagory(True)
            else:
                state_change()
                windowcreate.subcatagory(state_var.get(),True)
        else:
            global Name_Entry
            Submit.configure(state = 'disabled')
            messagebox.showerror("Unsuccessful", "Invaild Format") 
            Submit.configure(state = 'enabled')
            if edit:
                Name_Entry.delete(0,tb.END)
                Name_Entry.insert(0,edit[2])
            addacc.focus_force()
        if not edit:
            name_var.set("")
            color_var.set("")
            email_var.set("")
            password_var.set("")
    def form(edit = False):
        if not addwindow.get() and not editwindow.get() and not subcatagory.get():
            global widget_info,Submit,addacc,Name_Entry
            addwindow.set(True)
            canscroll_var.set(False)
            addacc = Toplevel(root)
            deffont = ('Helvetica', 18)
            deffant = ('Helvetica', 14)
            # addacc.resizable(False, False)
            addacc.protocol("WM_DELETE_WINDOW", lambda: (addwindow.set(False) , addacc.destroy(),canscroll_var.set(True)))
            Name_Label = tb.Label(addacc, text='Name:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
            Name_Label.grid(column=0,row=0)
            Email_Label = tb.Label(addacc, text='Email:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
            Password_Label = tb.Label(addacc, text='Pass:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
            Color_Label = tb.Label(addacc, text='Color:',style=PRIMARY,font=deffont,foreground="#C0C0C0")
            Password_Entry = tb.Entry(addacc,width=15,font=deffant,textvariable=password_var)
            Name_Entry = tb.Entry(addacc,width=15,textvariable=name_var,font=deffant)
            Email_Entry = tb.Entry(addacc,width=15,font=deffant,textvariable=email_var)
            original_image = Image.open("color_icon_transparent.png") 
            resized_image = original_image.resize((30, 30))
            icon = ImageTk.PhotoImage(resized_image) 
            colorpicker = tb.Button(addacc, image=icon, bootstyle="link",takefocus=False, padding=0, cursor="hand2", command= lambda:colorpicking(addacc))
            colorpicker.image = icon
            Name_Entry.grid(column=1,row=0,pady=10,padx=5)
            addacc.option_add('*TCombobox*Listbox.font', ('Helvetica', 14))
            Submit = tb.Button(addacc,takefocus=False,width=10,style='Custom.TButton',text="Submit",command=lambda:(ADD.submit(edit)))
            Email_Entry.delete(0, tb.END)
            Name_Entry.delete(0, tb.END)
            Password_Entry.delete(0, tb.END)
            color_var.set("6e40c0")
            if edit:
                color_var.set(edit[5])
                if state_bool.get():
                    Name_Entry.insert(0,edit[2])
                    Email_Entry.insert(0,edit[3])
                    Password_Entry.insert(0,edit[4])
                else:
                    Name_Entry.insert(0,edit[2] if not edit[3] else edit[3])
            if not state_bool.get():
                Submit.place(x=85,y=110)
                addacc.title("Add Catagory")
                reso = center(275,150)
                addacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            else:
                Email_Label.grid(column=0,row=1)
                Email_Entry.grid(column=1,row=1,pady=10,padx=5)
                Password_Entry.grid(column=1,row=2,pady=10,padx=5)
                Password_Label.grid(column=0,row=2)
                Submit.place(x=143,y=175)
                Color_Label.place(x=5,y=175)
                colorpicker.place(x=78, y=173)
                reso = center(275,230)
                addacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            style = tb.Style()
            style.configure('Custom.TCheckbutton', font=('Helvetica', 18),foreground='#C0C0C0')
class EDIT:
    def standard():
        global editwindow,addwindow,editacc
        if not editwindow.get() and not addwindow.get() and not subcatagory.get():
            editwindow.set(True)
            canscroll_var.set(False)
            editacc = Toplevel(root)
            reso = center(450,300)
            editacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            editacc.resizable(False, False)
            editacc.protocol("WM_DELETE_WINDOW", lambda: (editwindow.set(False) , editacc.destroy(),canscroll_var.set(True)))
    def form():
        EDIT.standard()
    def remove(name):
        if not state_bool.get():
            cun.execute('''SELECT name FROM database WHERE cata = ?''', (name,))
            names = cun.fetchall()
            for i in range(len(names)):
                cun.execute('''DELETE FROM database WHERE cata = ? AND name = ?''',(name,names[i][0]))
            cun.execute('''DELETE FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (name,))
            windowcreate.catagory(True)
        else:
            cun.executemany('''DELETE FROM database WHERE cata= ? AND name = ?''',((state_var.get() , name),))
            for widget,method,info in subcata_info:
                widget.destroy()
            windowcreate.subcatagory(state_var.get())
        conn.commit()
    def edit(name): #could be catagory/subcatagory
        if state_bool.get():
            cun.execute('''SELECT * FROM database WHERE cata = ? AND name = ?''', (state_var.get(), name))
        else:
            cun.execute('''SELECT * FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (name,))

        ADD.form(cun.fetchone())
    def pop(e):
        menur.post(e.x_root, e.y_root)
def database(name,email,password,color, catagory,id):
    sql = ''' INSERT INTO database(name,email,password,color,cata,ID)
              VALUES(?,?,?,?,?,?) '''
    color_var.set("");
    comm = [(name, email, password,color,catagory,id),]
    cun.executemany(sql, comm)
    conn.commit()
class readbase():
    def countc():
        cun.execute('''
                    SELECT COUNT(cata) FROM database WHERE cata == 'false' and password = ''
                    ''')
        return cun.fetchone()[0]
    def countb(id):
        count = 0   
        cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2 AND cata = ?",(state_var.get(),))
        ID = cun.fetchall()
        temp = ""
        if int(id) >= 10:
            for i in range(len(ID)):
                temp = ""
                for j in range(len(ID[i][0])):
                    if ID[i][0][j] != "/":
                        temp += ID[i][0][j]
                    else:
                        break
                if temp == id:
                    count += 1
        else:
            for i in ID:
                if i[0][0] == id:
                    count += 1
        return count
class windowcreate(): #this will make it THAT window
    global cata_button,state_var,widget_info,subcata_info
    def catagory(update=False): # <=== this needs to be optimized
            if update:
                for button in cata_button:
                    button.destroy()
                for button,info in widget_info:
                    button.destroy()
            widget_info.clear()
            cun.execute("SELECT name FROM database WHERE cata = 'false' AND password = '' ")
            names = cun.fetchall()
            cun.execute("SELECT email FROM database WHERE cata = 'false' AND password = '' ")
            emails = cun.fetchall()
            update_scrollregion(0,update)
            for i in range(readbase.countc()):
                button = tb.Button(second_frame, text=f'{names[i][0] if not emails[i][0] else emails[i][0]}',takefocus=False,width=13,style='Custom.TButton')
                button.bind("<Button-3>",EDIT.pop)
                button.bind("<Button-3>", lambda event, g=names[i][0]: currentmenu_var.set(g), add="+")
                button.configure(command=lambda b = names[i][0]: windowcreate.subcatagory(b))
                if i % 2 == 0:
                    button.place(x=8, y = i*35)
                else:
                    button.place(x=179, y=(i-1)*35)
                widget_info.append((button, button.place_info()))
    def searchc(): 
        global search_name
        for button,info in widget_info:
            button.place_forget()
        for button in cata_button:
            button.destroy()
        cata_button.clear()
        for i in range(len(search_name)):
            cun.execute("SELECT email FROM database WHERE cata = 'false' AND password = '' AND LENGTH(email) > 0 AND name = ?", (search_name[i],))
            emails = cun.fetchall() or ""
            button = tb.Button(second_frame, text=f'{search_name[i] if (emails == "") else emails[0][0]}',takefocus=False,width=13,style='Custom.TButton')
            button.configure(command=lambda b = search_name[i]: windowcreate.subcatagory(b))
            button.bind("<Button-3>",EDIT.pop)
            button.bind("<Button-3>", lambda event, g=search_name[i]: currentmenu_var.set(g), add="+")
            if i % 2 == 0:
                button.place(x=8, y = i*35)
            else:
                button.place(x=179, y=(i-1)*35)
            cata_button.append(button)
        update_scrollregion(len(search_name))
    def searchb():
        for button in buttons2:
             button.destroy()
        buttons2.clear()
        for i in range(len(search_name)):
            button = tb.Button(second_frame, text=f'{search_name[i]}',takefocus=False,width=10,style='Custom.TButton')
            button.bind("<Button-3>",EDIT.pop)
            button.bind("<Button-3>", lambda event, g=search_name[i]: currentmenu_var.set(g), add="+")
            button.configure(command=lambda b = search_name[i]: windowcreate.form(state_var.get(),b))
            if i % 2 == 0:
                button.place(x=4, y = i*35)
            else:
                button.place(x=200, y=(i-1)*35)
            buttons2.append(button)
        update_scrollregion(len(search_name))
    def subcatagory(indic,update=False):
            global my_canvas,stater
            if (not editwindow.get() and not addwindow.get()) or update:
                cun.execute('''SELECT * FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (indic,))
                title = cun.fetchone()
                root.title(title[3] if title[3] else title[2])
                if (state_var.get()=="LLm" and add.cget("text")=="Add") or update:
                    for widget,info in widget_info:
                        widget.place_forget()
                    for button in cata_button:
                        button.place_forget()
                    root.geometry('335x450')
                if state_var.get() != indic:
                    state_var.set(indic)
                edit.config(text="Add",command=lambda:(ADD.form()))
                add.config(text="Back",command=lambda:default_page("previous"))
                cun.execute("SELECT ID FROM database WHERE name = ? AND cata = ?", (indic,"false"))
                id = cun.fetchone()[0]
                # subcata.resizable(False, False)
                second_frame.configure(width=325, height=readbase.countb(id) * 35) #50*45, 45 is y for each button and 50 is number of button
                my_canvas.configure(width = 100, height = 150)
                cun.execute("SELECT name FROM database WHERE LENGTH(ID) > 2 AND cata = ?",(indic,))
                subnames = list(cun.fetchall())
                cun.execute("SELECT color FROM database WHERE cata = ?", (indic,))
                style = tb.Style()
                color = list(cun.fetchall())
                for i in range(readbase.countb(id)):
                    main_color = "#"+color[i][0]
                    gray_highlight = "#{:02X}{:02X}{:02X}".format(*(int(int(main_color[i:i+2], 16) * 0.9) for i in (1, 3, 5)))
                    style.configure(f"Color{i}.TButton",
                    background=main_color,
                    bordercolor="#8B0000",
                    borderwidth=3,
                    font=("Helvetica", 12,),
                    relief="flat",
                    border_width=3,
                    border_spacing=10,
                    corner_radius=50
                    )
                    style.map(f"Color{i}.TButton",
          background=[("active", gray_highlight), ("pressed", "#8B0000")],  # Keeps button red
          foreground=[("active", "white"), ("pressed", "white")],  # Keeps text white
          bordercolor=[("active", "#8B0000"), ("pressed", "#8B0000")])  # Keeps border red
                    button = tb.Button(second_frame, text=f'{subnames[i][0]}',takefocus=False,width=10,style=f"Color{i}.TButton")
                    subcata_info.append((button, 'place', button.place_info()))
                    button.configure(command=lambda b = subnames[i][0]: windowcreate.form(indic,b))
                    button.bind("<Button-3>",EDIT.pop)
                    button.bind("<Button-3>", lambda event, g=subnames[i][0]: currentmenu_var.set(g), add="+")
                    if i % 2 == 0:
                        button.place(x=4, y = i*35)
                    else:
                        button.place(x=200, y=(i-1)*35)
                    buttons2.append(button)
                update_scrollregion(len(subnames),update)
                text_var.trace_remove('write', stater)
                text_var.set("")
                stater = text_var.trace_add("write", on_text_change)
    def form(indic,subcata):
        global editwindow,addwindow,subcatagory
        if not subcatagory.get() and not editwindow.get() and not addwindow.get():
            root.withdraw()
            cun.execute("SELECT ID,name,email,password FROM database WHERE name = ? AND cata = ?", (subcata,indic))
            deffont = ('Helvetica',18)
            info = cun.fetchone()
            subcatagory.set(True)
            canscroll_var.set(False)
            subcat = Toplevel(root)
            subcat.attributes("-topmost", True)
            subcat.title(subcata)
            reso = center(300,125)
            subcat.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            # subcat.resizable(False, False) 
            style = tb.Style()
            style.configure("TEntry", selectbackground="#191830")
            username = tb.Label(subcat,text="Name: ",takefocus=False,width=7,style=PRIMARY,font=deffont,foreground="#C0C0C0")
            username_entry = tb.Entry(subcat,width=15,takefocus=False,style=PRIMARY,font=deffont)
            password = tb.Label(subcat,text="Pass: ",takefocus=False,width=7,style=PRIMARY,font=deffont,foreground="#C0C0C0")
            password_entry = tb.Entry(subcat,width=15,takefocus=False,style=PRIMARY,font=deffont)
            username_entry.insert(tb.END,info[2])
            password_entry.insert(tb.END,info[3])
            username_entry.config(state=tb.READONLY)
            password_entry.config(state=tb.READONLY)
            username.place(x=5,y=10)
            password.place(x=5,y=70)
            password_entry.place(x=85,y=65)
            username_entry.place(x=85,y=5)
            def copy(name=""):
                if name=="pass":
                     pyperclip.copy(info[3])
                else:
                    pyperclip.copy(info[2])
            username_entry.bind("<Button-1>",lambda event:copy())
            password_entry.bind("<Button-1>", lambda event: copy("pass"))
            subcat.protocol("WM_DELETE_WINDOW", lambda: (subcatagory.set(False) , subcat.destroy(),canscroll_var.set(True),root.deiconify()))
addwindow = BooleanVar()
editwindow = BooleanVar()
subcatagory = BooleanVar()
reso = center(335,450) 
root.geometry(f'{reso[0]}x{reso[1]}+{reso[2]}+{reso[3]}')
menur = tb.Menu(root,relief="flat",borderwidth=0)
menur.add_command(label="Edit", command=lambda:EDIT.edit(currentmenu_var.get()))
menur.add_command(label="Remove",command=lambda: EDIT.remove(currentmenu_var.get()))
def create(x,y):
    for i in range(1,x):
        database(f"cata{i}","","","6e40c0","false",f"{1}")
        for j in range(1,y):
            database(f"subcata{j}",f"kem{j}",f"kem{j}",f"6e40c0",f"cata{i}",f"{1}/1")
def default_page(name=""):
    global my_canvas,second_frame,edit,add,state_var,main_frame,search,stater
    root.title("Accounts")
    # root.resizable(False, False)
    if name == "previous" and state_bool.get() and not addwindow.get() and not editwindow.get():
        global state_var
        state_var.set("LLm")
        for widget,method,info in subcata_info:
            widget.destroy()
        for button in buttons2:
            button.destroy()
        editwindow.set(False)
        addwindow.set(False)
        root.geometry('335x450')
        edit.config(text='Edit',width=5,command=lambda:EDIT.form())
        add.config(text='Add',width=5,command=lambda:ADD.form())
        second_frame.configure(width=340, height=readbase.countc()*35) #50*45, 45 is y for each button and 50 is number of button
        my_canvas.configure(width=100, height=405)
        for widget,info in widget_info:
            widget.place(**info)
        text_var.trace_remove('write', stater)
        text_var.set("")
        stater = text_var.trace_add("write", on_text_change)
    elif name != "previous":
        buttons2.clear()
        main_frame = tb.Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = tb.Canvas(main_frame, width=100, height=405)
        root.configure(bg='#110833')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        my_scrollbar = tb.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        second_frame = Frame(my_canvas, width=340, height=readbase.countc()*35) #50*45, 45 is y for each button and 50 is number of button
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        my_canvas.bind_all("<MouseWheel>", on_mousewheel)  
        search = tb.Entry(root, textvariable=text_var,width=30)
        edit = tb.Button(root, text='Edit',takefocus=False,width=5,style=PRIMARY,command=lambda:EDIT.form())
        edit.pack(side='right', anchor='e')
        search.pack(side='right', anchor='w',expand=True,padx=15,pady=5)
        add = tb.Button(root, text='Add',takefocus=False,width=5,style=PRIMARY,command=lambda:ADD.form())
        add.pack(side='left', anchor='e')
        windowcreate.catagory()
    update_scrollregion(0,True)
default_page()
stater = text_var.trace_add("write", on_text_change)
state_var.trace_add("write", state_change)
root.mainloop()