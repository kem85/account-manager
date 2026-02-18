import ttkbootstrap as tb
import pyperclip
import sys # Make sure this is imported at the top!
import psutil
import os
import time
from tkinter import messagebox, BooleanVar, Toplevel, Frame, BOTH, LEFT, RIGHT, VERTICAL, Y
from ttkbootstrap.constants import PRIMARY, READONLY, END
from ttkbootstrap.style import Style
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from PIL import Image, ImageTk, ImageDraw
import sqlite3
from pystray import MenuItem as item, Icon
import threading
import keyboard
# Database Setup
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
height_var = tb.IntVar()
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
subcata_info = []
buttons = tb.Style()
search_name = []
cata_button = []
lst = []
buttons2 = []
iteration = ["False", 0]

buttons.configure('Custom.TButton', font=('Helvetica', 12), foreground='#C0C0C0')
if getattr(sys, 'frozen', False):
    # If the app is running as an .exe
    app_dir = sys._MEIPASS
else:
    # If running as a normal .py script
    app_dir = os.path.dirname(os.path.abspath(__file__))

ICON_PATH = os.path.join(app_dir, "color_icon_transparent.png")
DB_PATH = os.path.join(app_dir, 'accounts.db')
def center(x, y):
    rs = []
    rs.append(x)
    rs.append(y)
    rs.append(int(root.winfo_screenwidth()/2 - x/ 2))
    rs.append(int(root.winfo_screenheight()/2 - y/2))
    return rs

ICON_PATH = "color_icon_transparent.png"

def show_window():
    global tray_icon
    if state_bool.get():
        default_page("previous", True)
    root.deiconify()
    tray_icon.stop()

def hide_window():
    global tray_icon, iteration
    root.withdraw()
    iteration = ["True", 0]
    menu = (item('Show', show_window), item('Exit', exit_app))
    try:
        image = Image.open(ICON_PATH)
        tray_icon = Icon("TrayIcon", image, menu=menu)
        threading.Thread(target=tray_icon.run, daemon=True).start()
    except Exception as e:
        print(f"Tray icon error: {e}")

def exit_app():
    if 'tray_icon' in globals():
        tray_icon.stop()
    root.destroy()

def state_change(*args):
    global lst
    lst.clear()
    if add.cget("text") == "Back" and state_var.get() == "LLm":
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

def on_text_change(*args):
    global search_name, cata_button, lst
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

def on_mousewheel(event):
    if canscroll_var.get():
         my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def update_scrollregion(count = 0, update = False, tray = False):
    if count <= 0:      
        if not tray:      
            count = readbase.countc()
        else:
            count = (height_var.get())
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
    global addwindow, editwindow, widget_info
    def submit(edit = False):
        global Submit, addacc
        if not state_bool.get():
            cun.execute('''SELECT name FROM database WHERE cata == 'false' AND password = '' ''')
        else:
            cun.execute('''SELECT name FROM database WHERE cata = ? ''', (state_var.get(),))
        namer = cun.fetchall()
        filter_check = False
        for i in range(len(namer)):
            if (name_var.get() in namer[i]) and not (edit and name_var.get() == edit[2]):
                filter_check = True
        
        if not filter_check and ((len(color_var.get()) == 6) or color_var.get() == "") and name_var.get() != "" and ((email_var.get() != "" and password_var.get() !="" and state_bool.get()) or not state_bool.get()):
            global lst
            Submit.configure(state='disabled')
            text_var.set("")
            lst.append(name_var.get())
            messagebox.showinfo(title="Successful", message=f'{"Added" if not edit else "Edited"} {"Account" if state_bool.get() else "Category"} successfully')
            Submit.configure(state='enabled')
            addacc.focus_force()
            
            if not edit:
                if readbase.countc() != 0 and not state_bool.get():
                    id_var.set(f"{readbase.countc()+1}")
                elif not state_bool.get():
                    id_var.set("1")
                else:
                    count = 1
                    cun.execute("SELECT ID FROM database WHERE name = ?", (state_var.get(),))
                    res = cun.fetchone()
                    ID = res[0] if res else "1"
                    cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2")
                    for i in cun:
                        if i[0][0] == ID:
                            count += 1
                    id_var.set(f"{ID}/{count}")
                database(name_var.get(), email_var.get(), password_var.get(), color_var.get() or "6e40c0", "false" if not state_bool.get() else state_var.get(), id_var.get())
            else:
                if state_bool.get():
                    cun.execute('''UPDATE database SET name = ?, email = ?, password = ?, color = ? WHERE cata = ? AND name = ?''', (name_var.get(), email_var.get(), password_var.get(), color_var.get() if color_var.get() else "6e40c0", state_var.get(), edit[2]))
                else:
                    cun.execute("UPDATE database SET name = ?, color = ? WHERE cata = 'false' AND name = ?", (name_var.get(), color_var.get() if color_var.get() else "6e40c0", edit[2]))
            conn.commit()

            if not state_bool.get():
                windowcreate.catagory(True)
            else:
                state_change()
                windowcreate.subcatagory(state_var.get(), True)
        else:
            global Name_Entry
            Submit.configure(state='disabled')
            messagebox.showerror("Unsuccessful", "Invalid Format") 
            Submit.configure(state='enabled')
            if edit:
                Name_Entry.delete(0, END)
                Name_Entry.insert(0, edit[2])
            addacc.focus_force()
            
        if not edit:
            name_var.set("")
            color_var.set("")
            email_var.set("")
            password_var.set("")

    def form(edit = False):
        if not addwindow.get() and not editwindow.get() and not subcatagory.get():
            global widget_info, Submit, addacc, Name_Entry
            addwindow.set(True)
            canscroll_var.set(False)
            addacc = Toplevel(root)
            deffont = ('Helvetica', 18)
            deffant = ('Helvetica', 14)
            addacc.protocol("WM_DELETE_WINDOW", lambda: (addwindow.set(False), addacc.destroy(), canscroll_var.set(True)))
            
            Name_Label = tb.Label(addacc, text='Name:', style=PRIMARY, font=deffont, foreground="#C0C0C0")
            Name_Label.grid(column=0, row=0)
            Email_Label = tb.Label(addacc, text='Email:', style=PRIMARY, font=deffont, foreground="#C0C0C0")
            Password_Label = tb.Label(addacc, text='Pass:', style=PRIMARY, font=deffont, foreground="#C0C0C0")
            Color_Label = tb.Label(addacc, text='Color:', style=PRIMARY, font=deffont, foreground="#C0C0C0")
            
            Password_Entry = tb.Entry(addacc, width=15, font=deffant, textvariable=password_var)
            Name_Entry = tb.Entry(addacc, width=15, textvariable=name_var, font=deffant)
            Email_Entry = tb.Entry(addacc, width=15, font=deffant, textvariable=email_var)
            
            try:
                original_image = Image.open(ICON_PATH)
                resized_image = original_image.resize((30, 30))
                icon = ImageTk.PhotoImage(resized_image) 
                colorpicker = tb.Button(addacc, image=icon, bootstyle="link", takefocus=False, padding=0, cursor="hand2", command=lambda: colorpicking(addacc))
                colorpicker.image = icon
            except:
                colorpicker = tb.Button(addacc, text="CP", command=lambda: colorpicking(addacc))

            Name_Entry.grid(column=1, row=0, pady=10, padx=5)
            addacc.option_add('*TCombobox*Listbox.font', ('Helvetica', 14))
            Submit = tb.Button(addacc, takefocus=False, width=10, style='Custom.TButton', text="Submit", command=lambda: (ADD.submit(edit)))
            
            Email_Entry.delete(0, END)
            Name_Entry.delete(0, END)
            Password_Entry.delete(0, END)
            color_var.set("6e40c0")
            
            if edit:
                color_var.set(edit[5])
                if state_bool.get():
                    Name_Entry.insert(0, edit[2])
                    Email_Entry.insert(0, edit[3])
                    Password_Entry.insert(0, edit[4])
                else:
                    Name_Entry.insert(0, edit[2])
            
            if not state_bool.get():
                Submit.place(x=130, y=55)
                addacc.title("Add Category" if not edit else "Edit Category")
                reso = center(270, 100)
                Color_Label.place(x=0, y=55)
                colorpicker.place(x=79, y=53)
                addacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+150}')
            else:
                Email_Label.grid(column=0, row=1)
                Email_Entry.grid(column=1, row=1, pady=10, padx=5)
                Password_Entry.grid(column=1, row=2, pady=10, padx=5)
                Password_Label.grid(column=0, row=2)
                Submit.place(x=143, y=175)
                Color_Label.place(x=5, y=175)
                colorpicker.place(x=78, y=173)
                reso = center(275, 230)
                addacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')

class EDIT:
    def standard():
        global editwindow, addwindow, editacc
        if not editwindow.get() and not addwindow.get() and not subcatagory.get():
            editwindow.set(True)
            canscroll_var.set(False)
            editacc = Toplevel(root)
            reso = center(450, 300)
            editacc.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            editacc.resizable(False, False)
            editacc.protocol("WM_DELETE_WINDOW", lambda: (editwindow.set(False), editacc.destroy(), canscroll_var.set(True)))
    
    def form():
        EDIT.standard()

    def remove(name):
        response = messagebox.askyesno("Confirmation", f'Are you sure you want to remove {name}?')
        if response:
            if not state_bool.get():
                cun.execute('''SELECT name FROM database WHERE cata = ?''', (name,))
                names = cun.fetchall()
                for i in range(len(names)):
                    cun.execute('''DELETE FROM database WHERE cata = ? AND name = ?''', (name, names[i][0]))
                cun.execute('''DELETE FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (name,))
                windowcreate.catagory(True)
            else:
                cun.execute('''DELETE FROM database WHERE cata= ? AND name = ?''', (state_var.get(), name))
                for widget, method, info in subcata_info:
                    widget.destroy()
                windowcreate.subcatagory(state_var.get())
            conn.commit()

    def edit(name):
        if state_bool.get():
            cun.execute('''SELECT * FROM database WHERE cata = ? AND name = ?''', (state_var.get(), name))
        else:
            cun.execute('''SELECT * FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (name,))
        ADD.form(cun.fetchone())

    def pop(e):
        menur.post(e.x_root, e.y_root)

def database(name, email, password, color, category, id_val_param):
    sql = ''' INSERT INTO database(name, email, password, color, cata, ID) VALUES(?,?,?,?,?,?) '''
    color_var.set("")
    comm = [(name, email, password, color, category, id_val_param),]
    cun.executemany(sql, comm)
    conn.commit()

class readbase():
    def countc():
        cun.execute(''' SELECT COUNT(cata) FROM databaseWHERE cata == 'false' and password = '' ''')
        return cun.fetchone()[0]

    def countb(id_param):
        count = 0   
        cun.execute("SELECT ID FROM database WHERE LENGTH(ID) >= 2 AND cata = ?", (state_var.get(),))
        IDs = cun.fetchall()
        for i in IDs:
            if "/" in i[0]:
                if i[0].split("/")[0] == str(id_param):
                    count += 1
            elif i[0] == str(id_param):
                count += 1
        return count

class windowcreate():
    global cata_button, state_var, widget_info, subcata_info
    def catagory(update=False):
        if update:
            for button in cata_button:
                button.destroy()
            for button, info in widget_info:
                button.destroy()
        widget_info.clear()
        cun.execute("SELECT name, email, color FROM database WHERE cata = 'false' AND password = '' ")
        data = cun.fetchall()
        update_scrollregion(0, update)
        
        style = tb.Style()
        for i, (name, email, color_hex) in enumerate(data):
            main_color = f"#{color_hex}" 
            rgb = tuple(int(main_color[j:j+2], 16) for j in (1, 3, 5))
            gray_highlight = "#{:02X}{:02X}{:02X}".format(*(int(c * 0.9) for c in rgb))
            
            style.configure(f"Color{i}.TButton", background=main_color, font=("Helvetica", 12))
            style.map(f"Color{i}.TButton", background=[("active", gray_highlight)])

            button = tb.Button(second_frame, text=f'{name if not email else email}', takefocus=False, width=13, style=f"Color{i}.TButton")
            button.bind("<Button-3>", EDIT.pop)
            button.bind("<Button-3>", lambda event, g=name: currentmenu_var.set(g), add="+")
            button.configure(command=lambda b=name: windowcreate.subcatagory(b))
            
            if i % 2 == 0:
                button.place(x=8, y = i*35)
            else:
                button.place(x=179, y=(i-1)*35)
            widget_info.append((button, button.place_info()))

    def searchc(): 
        global search_name
        for button, info in widget_info:
            button.place_forget()
        for button in cata_button:
            button.destroy()
        cata_button.clear()
        style = tb.Style()
        for i in range(len(search_name)):
            cun.execute("SELECT email, color FROM database WHERE cata = 'false' AND password = '' AND name = ?", (search_name[i],))
            res = cun.fetchone()
            email, color_hex = res if res else ("", "6e40c0")
            main_color = "#" + color_hex
            style.configure(f"SearchC{i}.TButton", background=main_color, font=("Helvetica", 12))
            
            button = tb.Button(second_frame, text=f'{search_name[i] if not email else email}', takefocus=False, width=13, style=f'SearchC{i}.TButton')
            button.configure(command=lambda b=search_name[i]: windowcreate.subcatagory(b))
            button.bind("<Button-3>", EDIT.pop)
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
        style = tb.Style()
        for i in range(len(search_name)):
            cun.execute("SELECT color FROM database WHERE cata = ? AND name = ?", (state_var.get(), search_name[i]))
            res = cun.fetchone()
            color_hex = res[0] if res else "6e40c0"
            style.configure(f"SearchB{i}.TButton", background="#" + color_hex, font=("Helvetica", 12))
            
            button = tb.Button(second_frame, text=f'{search_name[i]}', takefocus=False, width=10, style=f'SearchB{i}.TButton')
            button.bind("<Button-3>", EDIT.pop)
            button.bind("<Button-3>", lambda event, g=search_name[i]: currentmenu_var.set(g), add="+")
            button.configure(command=lambda b=search_name[i]: windowcreate.form(state_var.get(), b))
            if i % 2 == 0:
                button.place(x=4, y = i*35)
            else:
                button.place(x=200, y=(i-1)*35)
            buttons2.append(button)
        update_scrollregion(len(search_name))

    def subcatagory(indic, update=False):
            global my_canvas, stater
            if (not editwindow.get() and not addwindow.get()) or update:
                cun.execute('''SELECT * FROM database WHERE name = ? AND cata = 'false' AND password = '' ''', (indic,))
                title = cun.fetchone()
                if title:
                    root.title(title[3] if title[3] else title[2])
                
                if (state_var.get() == "LLm" and add.cget("text") == "Add") or update:
                    for widget, info in widget_info:
                        widget.place_forget()
                    for button in cata_button:
                        button.place_forget()
                    root.geometry('335x450')
                
                if state_var.get() != indic:
                    state_var.set(indic)
                
                edit.config(text="Add", command=lambda: (ADD.form()))
                add.config(text="Back", command=lambda: default_page("previous"))
                
                cun.execute("SELECT ID FROM database WHERE name = ? AND cata = ?", (indic, "false"))
                res_id = cun.fetchone()
                db_id = res_id[0] if res_id else "1"
                
                second_frame.configure(width=325, height=readbase.countb(db_id) * 35)
                my_canvas.configure(width = 100, height = 150)
                
                cun.execute("SELECT name, color FROM database WHERE LENGTH(ID) > 2 AND cata = ?", (indic,))
                sub_data = cun.fetchall()
                style = tb.Style()
                
                for i, (s_name, s_color) in enumerate(sub_data):
                    style.configure(f"Sub{i}.TButton", background="#" + s_color, font=("Helvetica", 12))
                    button = tb.Button(second_frame, text=s_name, takefocus=False, width=10, style=f"Sub{i}.TButton")
                    subcata_info.append((button, 'place', button.place_info()))
                    button.configure(command=lambda b=s_name: windowcreate.form(indic, b))
                    button.bind("<Button-3>", EDIT.pop)
                    button.bind("<Button-3>", lambda event, g=s_name: currentmenu_var.set(g), add="+")
                    
                    if i % 2 == 0:
                        button.place(x=4, y = i*35)
                    else:
                        button.place(x=200, y=(i-1)*35)
                    buttons2.append(button)
                
                update_scrollregion(len(sub_data), update)
                text_var.trace_remove('write', stater)
                text_var.set("")
                stater = text_var.trace_add("write", on_text_change)

    def form(indic, subcata):
        global editwindow, addwindow, subcatagory, iteration
        iteration = ["False", 0]
        if not subcatagory.get() and not editwindow.get() and not addwindow.get():
            root.withdraw()
            cun.execute("SELECT ID, name, email, password FROM database WHERE name = ? AND cata = ?", (subcata, indic))
            info = cun.fetchone()
            if not info: return
            
            deffont = ('Helvetica', 18)
            subcatagory.set(True)
            canscroll_var.set(False)
            subcat = Toplevel(root)
            subcat.attributes("-topmost", True)
            subcat.title(subcata)
            reso = center(300, 125)
            subcat.geometry(f'{reso[0]}x{reso[1]}+{root.winfo_x()+30}+{root.winfo_y()+100}')
            
            username = tb.Label(subcat, text="Name: ", takefocus=False, width=7, style=PRIMARY, font=deffont, foreground="#C0C0C0")
            username_entry = tb.Entry(subcat, width=15, takefocus=False, style=PRIMARY, font=deffont)
            password_lbl = tb.Label(subcat, text="Pass: ", takefocus=False, width=7, style=PRIMARY, font=deffont, foreground="#C0C0C0")
            password_entry = tb.Entry(subcat, width=15, takefocus=False, style=PRIMARY, font=deffont)
            
            username_entry.insert(END, info[2])
            password_entry.insert(END, "dont peak")
            username_entry.config(state=READONLY)
            password_entry.config(state=READONLY)
            
            username.place(x=5, y=10)
            password_lbl.place(x=5, y=70)
            password_entry.place(x=85, y=65)
            username_entry.place(x=85, y=5)
            
            def paste():
                if iteration[0] == "False" and iteration[1] == 0:
                    pyperclip.copy(info[2])
                    iteration[1] = 1
                elif iteration[0] == "False" and iteration[1] == 1:
                    pyperclip.copy(info[3])
                    iteration[1] = 0
            
            def copy_val(target=""):
                iteration[0] = "True"
                if target == "pass":
                     pyperclip.copy(info[3])
                else:
                    pyperclip.copy(info[2])
            
            # Clear existing ctrl+v to prevent duplicates
            try: keyboard.remove_hotkey("ctrl+v")
            except: pass
            keyboard.add_hotkey("ctrl+v", paste)
            username_entry.bind("<Button-1>", lambda event: copy_val())
            password_entry.bind("<Button-1>", lambda event: copy_val("pass"))
            subcat.protocol("WM_DELETE_WINDOW", lambda: (subcatagory.set(False), subcat.destroy(), canscroll_var.set(True), root.deiconify()))

addwindow = BooleanVar()
editwindow = BooleanVar()
subcatagory = BooleanVar()
reso_main = center(335, 450) 
root.geometry(f'{reso_main[0]}x{reso_main[1]}+{reso_main[2]}+{reso_main[3]}')

menur = tb.Menu(root, relief="flat", borderwidth=0)
menur.add_command(label="Edit", command=lambda: EDIT.edit(currentmenu_var.get()))
menur.add_command(label="Remove", command=lambda: EDIT.remove(currentmenu_var.get()))

def default_page(name="", tray = False):
    global my_canvas, second_frame, edit, add, state_var, main_frame, search, stater
    root.title("Accounts")
    if name == "previous" and state_bool.get() and not addwindow.get() and not editwindow.get():
        state_var.set("LLm")
        for widget, method, info in subcata_info:
            widget.destroy()
        for button in buttons2:
            button.destroy()
        editwindow.set(False)
        addwindow.set(False)
        root.geometry('335x450')
        edit.config(text='Edit', width=5, command=lambda: EDIT.form())
        add.config(text='Add', width=5, command=lambda: ADD.form())
        second_frame.configure(width=340, height=readbase.countc()*35 if not tray else height_var.get()) 
        if not tray:
            height_var.set(readbase.countc()*35)
        my_canvas.configure(width=100, height=405)
        for widget, info in widget_info:
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
        
        second_frame = Frame(my_canvas, width=340, height=(readbase.countc()*35))
        height_var.set(readbase.countc()*35)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        my_canvas.bind_all("<MouseWheel>", on_mousewheel)  
        
        search = tb.Entry(root, textvariable=text_var, width=30)
        edit = tb.Button(root, text='Edit', takefocus=False, width=5, style=PRIMARY, command=lambda: EDIT.form())
        edit.pack(side='right', anchor='e')
        search.pack(side='right', anchor='w', expand=True, padx=15, pady=5)
        add = tb.Button(root, text='Add', takefocus=False, width=5, style=PRIMARY, command=lambda: ADD.form())
        add.pack(side='left', anchor='e')
        windowcreate.catagory()
    
    if not tray:
        update_scrollregion(0, True)
    else:
        update_scrollregion(0, True, True)

default_page()
keyboard.add_hotkey("ctrl+alt+x", show_window)  
stater = text_var.trace_add("write", on_text_change)
state_var.trace_add("write", state_change)
root.protocol("WM_DELETE_WINDOW", hide_window)
root.protocol("WM_MINIMIZE", hide_window)

uptime_seconds = time.time() - psutil.boot_time()
if uptime_seconds < 300:
    root.after(100, hide_window)

root.mainloop()