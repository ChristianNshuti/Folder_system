import tkinter as tk
from tkinter import filedialog
import os
import shutil 
import subprocess
import math
from tkinter import ttk
from PIL import Image,ImageTk

def create_folder():
    folder_name = createEntry.get().strip()

    if folder_name == "":
        status_label.config(text='Please enter a folder name!',fg="red")
        return

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        status_label.config(text=f'{folder_name} created!', fg="green")
    else:
        status_label.config(text=f'{folder_name} already exists', fg="yellow")
    
    list_folders_tree()

def delete_folder():
    item_name = createEntry.get().strip()

    if item_name == "":
        status_label.config(text="Please enter a folder name!",fg="red")
        return

    if os.path.exists(item_name):
        if os.path.isdir(item_name):
            shutil.rmtree(item_name)
            status_label.config(text=f'{item_name} was removed successfully!',fg="green")
        else:
            os.remove(item_name)
            status_label.config(text=f'{item_name} was removed successfully!',fg="green")
    else:
        status_label.config(text="Folder does not exist",fg="red")

    list_folders_tree()

def rename_folder():
    folder_name = createEntry.get().strip()
    new_folder_name = renameEntry.get().strip()

    if new_folder_name == "":
        status_label.config(text="Please enter a folder name",fg="red")
        return
    
    if os.path.exists(new_folder_name):
        status_label.config(text=f'Folder with name {new_folder_name} already exists!',fg="red")
        return
    
    if os.path.exists(folder_name):
        os.rename(folder_name,new_folder_name)
        status_label.config(text=f'{folder_name} renamed to {new_folder_name}',fg="green")

    else:
        status_label.config(text="Folder does not exist",fg="red")

    list_folders_tree()



def open_in_terminal():
    try:
        selected = folder_tree.selection()
        full_path = folder_tree.item(selected[0])["values"][0]
        if os.path.exists(full_path):
            subprocess.Popen(f'start cmd /K cd "{full_path}"',shell=True)

    except:
        status_label.config(text="Please select a folder first!", fg="red")

def fill_entry(event):
        selected = folder_tree.selection()
        createEntry.delete(0,tk.END)
        createEntry.insert(0,folder_tree.item(selected[0])["text"])

def choose_directory():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        list_folders_tree()

def search_folder(event):
    query = searchEntry.get().strip().lower()
    folder_tree.delete(*folder_tree.get_children())

    for root,dirs,files in os.walk(os.getcwd()):
            for name in dirs + files:
                if query in name.lower():
                    full_path = os.path.join(root,name)
                    icon = folder_icon_tk if os.path.isdir(full_path) else file_icon_tk
                    folder_tree.insert("","end",text=name,values=[full_path],image=icon)

def show_info(event):
    selected = folder_tree.selection()
    if not selected:
        return
    
    item_name = folder_tree.item(selected[0])["text"]
    full_path = folder_tree.item(selected[0])["values"][0]
    if os.path.exists(full_path):
        if os.path.isdir(full_path):
            size = folder_size(full_path)
            num_files = len(os.listdir(full_path))
            status_label.config(text=f'Selected: {item_name} : {num_files} files : {size} mb',fg="black")
        else:
            size = math.ceil(os.path.getsize(full_path) / (1024*1024))
            status_label.config(text=f'Selected: {item_name} : {size} mb',fg="black")
        

def folder_size(path):
    total = 0
    for root,dirs,files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root,f))
    return math.ceil(total / (1024 * 1024))

def insert_children(parent_node,parent_path):
    try:
        for item in os.listdir(parent_path):
            full_path = os.path.join(parent_path,item)
            if os.path.isdir(full_path):
                node = folder_tree.insert(
                    parent_node,
                    "end",
                    text=item,
                    values=[full_path],
                    image=folder_icon_tk
                )

                insert_children(node,full_path)

            else:
                node = folder_tree.insert(
                    parent_node,
                    "end",
                    text=item,
                    values=[full_path],
                    image=file_icon_tk
                )

    except PermissionError:
        pass

def list_folders_tree():
    folder_tree.delete(*folder_tree.get_children())
    path = os.getcwd()
    node = folder_tree.insert(
        "",
        "end",
        text=os.path.basename(path),
        values=[path],
        image=folder_icon_tk,
    )
    insert_children(node,path)
    folder_tree.item(node,open=True)


def on_folder_select(event):
    selected_item = folder_tree.selection()
    if selected_item:
        folder_name = folder_tree.item(selected_item[0])["text"]
        createEntry.delete(0,tk.END)
        createEntry.insert(0,folder_name)

def open_folder_tree(event):
    selected_item = folder_tree.selection()
    if selected_item:
        full_path = folder_tree.item(selected_item[0])["values"][0]
        subprocess.Popen(f'explorer "{full_path}"',shell=True)

def show_context_menu(event):
    selected_item = folder_tree.identify_row(event.y)
    if selected_item:
        folder_tree.selection_set(selected_item)
        context_menu.post(event.x_root,event.y_root)

def get_selected_item_name():
    selected = folder_tree.selection()
    if not selected:
        return None
    return folder_tree.item(selected[0])["values"][0]

def open_selected_item():
    selected_item = get_selected_item_name()
    if not selected_item:
        return 
    if os.path.isdir(selected_item):
        subprocess.Popen(f'explorer "{selected_item}"',shell=True)
    else:
        os.startfile(selected_item)

def rename_selected_item():
    selected_item = get_selected_item_name()
    if not selected_item:
        return 
    new_name= tk.simpledialog.askstring("Rename",f"Enter a new name for {selected_item}")
    if new_name:
        if os.path.exists(new_name):
            status_label.config(text=f"'{new_name}' already exists!",fg="red")
            return
        else:
            os.rename(selected_item,new_name)
            status_label.config(text=f"'{selected_item}' was renamed to '{new_name}'",fg="green")
            list_folders_tree()
    if not new_name:
        status_label.config(text=f'Please enter a file name',fg="red")

def delete_selected_item():
    selected_item = get_selected_item_name()
    if not selected_item:
        return 
    
    if os.path.isdir(selected_item):
        shutil.rmtree(selected_item)
    
    else:
        os.remove(selected_item)
    
    status_label.config(text=f"'{selected_item}' was removed successfully!",fg="green")
    list_folders_tree()

def show_selected_info():
    selected_item = get_selected_item_name()
    if not selected_item:
        return

    if os.path.exists(selected_item):
        if os.path.isdir(selected_item):
            size = folder_size(selected_item)
            num_files = len(os.listdir(selected_item))
            status_label.config(text=f'Selected: {selected_item} : {num_files} files : {size} mb')
        else:
            size = math.ceil(os.path.getsize(selected_item) / (1024*1024))
            status_label.config(text=f'Selected: {selected_item} : {size} mb')

def start_drag(event):
    global dragged_item
    global drag_start_y
    drag_start_y = event.y
    selected_item = folder_tree.selection()
    if not selected_item:
        return
    dragged_item = folder_tree.item(selected_item[0])["values"][0]

def dragging(event):
    pass

def drop_item(event):
    global dragged_item
    global drag_start_y
    if not dragged_item:
        return
    
    if abs(event.y - drag_start_y) > 5:
        target_item = folder_tree.identify_row(event.y)
        print("Dropped the item")
        print("Current target item: ",target_item)
        if target_item:
            target_folder = folder_tree.item(target_item)["values"][0]

            if os.path.isfile(target_folder):
                target_folder = os.path.dirname(target_folder)

            if target_folder.startswith(dragged_item):
                status_label.config(text="Can not move a folder into itself",fg="red")
                dragged_item = None
                return

            if dragged_item != target_folder:
                try:
                    shutil.move(dragged_item,target_folder)
                    list_folders_tree()
                    status_label.config(text=f"'{dragged_item}' was moved into '{target_folder}'")
                except Exception as e:
                    status_label.config(text=f"Error: {e}",fg="red")

            dragged_item = None

def create_file():
    file_name = createEntry.get()
    file_type = file_type_var.get()

    if file_name == "":
        status_label.config(text="Please enter a file name!",fg="red")
        return
    
    full_name = f'{file_name}.{file_type}'

    if os.path.exists(full_name):
        status_label.config(text="File already exists!")
        return 
    
    try:
        with open(full_name,'w') as f:
            pass

        status_label.config(text=f'{full_name} created successfully!',fg="green")
        list_folders_tree()

    except Exception as e:
        status_label.config(text=f"error '{e}'",fg="red")


        





dragged_item = None
drag_start_y = None

window = tk.Tk()
window.title("Folder system app")
window.geometry("500x900")

folder_icon = Image.open("./assets/folder.png")
folder_icon = folder_icon.resize((20,20))
folder_icon_tk = ImageTk.PhotoImage(folder_icon)

file_icon = Image.open("./assets/file.png")
file_icon = file_icon.resize((20,20))
file_icon_tk = ImageTk.PhotoImage(file_icon)

file_type_var = tk.StringVar(value="txt")



# frames below ---

top_frame = tk.Frame(window,padx=10,pady=10)
top_frame.pack(fill="x")

button_frame = tk.Frame(window,padx=10,pady=10)
button_frame.pack(fill="x")

tree_frame = tk.Frame(window,padx=10,pady=10)
tree_frame.pack(fill="x")

status_frame = tk.Frame(window,padx=10,pady=10)
status_frame.pack(fill="x")

tk.Label(top_frame,text="Folder/File name:").grid(row=0,column=0,sticky="w")
createEntry = tk.Entry(top_frame,width=20)
createEntry.grid(row=0,column=1,sticky="ew",padx=5)
top_frame.columnconfigure(1,weight=1)

tk.Label(top_frame,text="File type:").grid(row=1,column=0,sticky="w")
file_type_menu = tk.OptionMenu(top_frame,file_type_var,"csv","py","md","json","doc","docs","pptx","pdf")
file_type_menu.grid(row=1,column=1,sticky="w",padx=5)

tk.Label(top_frame,text="New folder/file name (renaming):").grid(row=2,column=0,sticky="w")
renameEntry = tk.Entry(top_frame,width=20)
renameEntry.grid(row=2,column=1,sticky="ew",padx=5)

tk.Label(top_frame,text="Search:").grid(row=3,column=0,sticky="w")
searchEntry = tk.Entry(top_frame,width=30)
searchEntry.grid(row=3,column=1,sticky="ew",padx=5)

createBtn = tk.Button(button_frame, text="Create Folder", command=create_folder)
createBtn.grid(row=0,column=0,padx=5,pady=5)
createFileBtn = tk.Button(button_frame,text="Create File",command=create_file)
createFileBtn.grid(row=0,column=1,padx=5,pady=5)
deleteBtn = tk.Button(button_frame, text="Delete Folder/File",command=delete_folder)
deleteBtn.grid(row=0,column=2,padx=5,pady=5)
renameBtn = tk.Button(button_frame,text="Rename Folder/File",command=rename_folder)
renameBtn.grid(row=0,column=3,padx=5,pady=5)
openInTerminalBtn = tk.Button(button_frame,text="Open directory in terminal",command=open_in_terminal)
openInTerminalBtn.grid(row=0,column=4,padx=5,pady=5)
chooseDirectoryBtn = tk.Button(button_frame,text="Choose directory",command=choose_directory)
chooseDirectoryBtn.grid(row=0,column=5,padx=5,pady=5)


folder_tree = ttk.Treeview(tree_frame,show='tree')
scrollbar = tk.Scrollbar(tree_frame)
folder_tree.config(yscrollcommand=scrollbar.set)
folder_tree.pack(side="left",fill="both",expand=True)
scrollbar.config(command=folder_tree.yview)
scrollbar.pack(side="right",fill="y")

status_label = tk.Label(status_frame,text="")
status_label.pack(fill="x")


context_menu = tk.Menu(window,tearoff=0)
context_menu.add_command(label="Open",command=lambda:open_selected_item())
context_menu.add_command(label="Rename",command=lambda:rename_selected_item())
context_menu.add_command(label="Delete",command=lambda:delete_selected_item())
context_menu.add_separator()
context_menu.add_command(label="Properties",command=lambda:show_selected_info())

searchEntry.bind("<KeyRelease>",search_folder)

folder_tree.bind("<Double-1>",open_folder_tree)
folder_tree.bind("<<TreeviewSelect>>",on_folder_select,add='+')
folder_tree.bind("<<TreeviewSelect>>",show_info,add='+')
folder_tree.bind("<Button-3>",show_context_menu)
folder_tree.bind("<ButtonPress-1>",start_drag)
folder_tree.bind("<B1-Motion>",dragging)
folder_tree.bind("<ButtonRelease-1>",drop_item)

list_folders_tree()

window.mainloop()