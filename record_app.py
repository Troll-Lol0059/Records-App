import sqlite3
import tkinter
from tkinter import *
import customtkinter
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import messagebox

customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
customtkinter.set_appearance_mode("dark")

class Record_App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        app_width = 850
        app_height = 600
        #grab screen width
        screen_Width = self.winfo_screenwidth()
        #grab screen height
        screen_height = self.winfo_screenheight()

        x = (screen_Width/2) - (app_width/2)
        y = (screen_height/2) - (app_height/2)

        self.title("Keep Records")
        self.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.configure(bg=("white","#3A3B3C"))

        self.main_window_frame = customtkinter.CTkFrame(master=self,fg_color=("#3A3B3C"),width=55,border_width=1,border_color="SILVER")
        self.main_window_frame.pack(side=LEFT,fill=Y)

        self.menu_bar = Menu(master=self,bg="grey",activebackground="#3A3B3C")
        self.config(menu=self.menu_bar)
        # mode menu 
        # self.mode_menu = Menu(self.menu_bar,tearoff=0,bg="grey",activebackground="#3A3B3C")
        # self.mode_menu.add_command(label = "Dark Mode",command= self.dark_mode)
        # self.mode_menu.add_command(label = "Light Mode",command= self.light_mode)
        # self.menu_bar.add_cascade(label = "Modes",menu=self.mode_menu)
        #sub menu of add
        self.add_sub_menu = Menu(tearoff=0,bg="grey",activebackground="#3A3B3C")
        self.add_sub_menu.add_command(label="GST",command=lambda:self.add_gst_details(window_name ="add_gst_window",window_title="Add Party GST Details",inner_title="Add GST Login Details",need_buttons="yes"))
        self.add_sub_menu.add_command(label="TDS",command=lambda:self.add_tds_details_window(window_name="add_tds_details",window_title="Add TDS Details",inner_title="ADD TDS DETAILS",need_buttons="yes"))
        self.add_sub_menu.add_command(label="Income Tax")
        # Add menu
        self.add_menu = Menu(self.menu_bar,tearoff=0,bg="grey",activebackground="grey")
        self.add_menu.add_cascade(label = "Login Details",menu=self.add_sub_menu)
        self.menu_bar.add_cascade(label = "Add",menu=self.add_menu)

        self.image1 = Image.open("gst_img.jpg")
        self.gst_button_image = ImageTk.PhotoImage(self.image1)

        self.image2 = Image.open("tds_img.png")
        self.tds_button_image = ImageTk.PhotoImage(self.image2)

        self.image3 = Image.open("it_tax.png")
        self.it_button_image = ImageTk.PhotoImage(self.image3)

        self.image4 = Image.open("settings_button.png")
        self.setting_button_image = ImageTk.PhotoImage(self.image4)

        self.gst_view_button = customtkinter.CTkButton(master=self.main_window_frame,text="GST",command=self.view_gst_records,compound=TOP,image=self.gst_button_image,width=55,height=15,fg_color=("#3A3B3C","#3A3B3C"),hover_color=("GREY","green"))
        self.gst_view_button.grid(row=0,column=0,sticky=W,pady=10,padx=5)

        self.tds_view_button = customtkinter.CTkButton(master=self.main_window_frame,text="TDS",compound=TOP,image=self.tds_button_image,width=38,height=15,fg_color=("#3A3B3C","#3A3B3C"),hover_color=("GREY","green"),command=self.create_tree_view)
        self.tds_view_button.grid(row=1,column=0,sticky=W,pady=10,padx=5)

        self.it_view_button = customtkinter.CTkButton(master=self.main_window_frame,text="IT",compound=TOP,image=self.it_button_image,width=38,height=15,fg_color=("#3A3B3C","#3A3B3C"),hover_color=("GREY","green"))
        self.it_view_button.grid(row=2,column=0,sticky=W,pady=10,padx=5)

        self.settings_button = customtkinter.CTkButton(master=self.main_window_frame,text="",image=self.setting_button_image,height=20,width=55,fg_color=("#3A3B3C","#3A3B3C"),hover_color=("GREY","green"))
        self.settings_button.grid(row=3,column=0,sticky=W,pady=(270,20),padx=5)

        # GST SEARCH,CLOSE BUTTON FRAME
        self.gst_view_frame2 = customtkinter.CTkFrame(master=self,height=50,fg_color=("white","#3A3B3C"),bg_color=("white","#3A3B3C"))
        self.gst_view_frame2.pack(side=TOP,anchor="n",fill=X)
        # GST TreeView Frame
        self.tree_view_frame = customtkinter.CTkFrame(master=self,fg_color=("white","#3A3B3C"),bg_color=("white","#3A3B3C"))
        self.tree_view_frame.pack(fill=BOTH,anchor="n")
        # TDS SEARCH,CLOSE BUTTON FRAME
        self.tds_tree_view_frame2 = customtkinter.CTkFrame(master=self,height=50,fg_color=("white","#3A3B3C"),bg_color=("white","#3A3B3C"))
        self.tds_tree_view_frame2.pack(side=TOP,anchor="n",fill=X)
        #TDS SEARCH VIEW FRAME
        self.tds_tree_view_frame = customtkinter.CTkFrame(master=self,fg_color=("white","#3A3B3C"),bg_color=("white","#3A3B3C"))
        self.tds_tree_view_frame.pack(fill=BOTH,anchor="n")


    def dark_mode(self):
        customtkinter.set_appearance_mode("dark")

    def light_mode(self):
        customtkinter.set_appearance_mode("light")
    
    def add_data(self):
        #connecting to database
        self.conn = sqlite3.connect('pathak_jii_database.db')
        #create a cursor
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO details VALUES (:party_name,:gst_no,:gst_id,:gst_password)", 
        {
            'party_name':self.gst_party_name_entry.get(), 
            'gst_no':self.gst_no_entry.get(),
            'gst_id':self.gst_id_entry.get(),
            'gst_password':self.gst_password_entry.get()
        })
        #commit changes
        self.conn.commit()
        #close database
        self.conn.close()
        self.clear_fields()
        w_name.destroy()

    def gst_window_close_button(self):
        self.gst_view_frame2.destroy()
        self.tree_view_frame.destroy()

    def view_gst_records(self):
        self.gst_view_frame2.destroy()
        self.tds_tree_view_frame.destroy()
        self.tree_view_frame.destroy()
        self.tds_tree_view_frame2.destroy()

        self.gst_view_frame2 = customtkinter.CTkFrame(master=self,height=50)
        self.gst_view_frame2.pack(side=TOP,anchor="n",fill=X)

        self.tree_view_frame = customtkinter.CTkFrame(master=self,fg_color="white",bg_color="white")
        self.tree_view_frame.pack(fill=BOTH)

        #styling tree
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="#D3D3D3",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="#D3D3D3")
        #create treeview frame
        #add a scroll bar
        self.tree_scroll = Scrollbar(self.tree_view_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        #create treeview
        self.tree_view = ttk.Treeview(self.tree_view_frame,yscrollcommand=self.tree_scroll.set)
        self.tree_view.pack(fill=BOTH,anchor="n")
        #Configure the scrollbar
        self.tree_scroll.config(command=self.tree_view.yview)
        #define treeview column
        self.tree_view['columns'] = ('RECORD ID','PARTY NAME','GST NO.','LOGIN ID','PASSWORD')
        #formate our columns
        self.tree_view.column("#0",width=0,anchor=CENTER,stretch=NO)
        self.tree_view.column("RECORD ID",width=45,anchor=CENTER)
        self.tree_view.column("PARTY NAME",anchor=CENTER,width=120)
        self.tree_view.column("GST NO.",anchor=CENTER,width=105)
        self.tree_view.column("LOGIN ID",anchor=CENTER,width=80)
        self.tree_view.column("PASSWORD",anchor=CENTER,width=80)
 
        #giving column headings
        self.tree_view.heading("#0",text="",anchor=W)
        self.tree_view.heading("#1",text="RECORD ID",anchor=W)
        self.tree_view.heading("#2",text="PARTY NAME",anchor=CENTER)
        self.tree_view.heading("#3",text="GST NO.",anchor=CENTER)
        self.tree_view.heading("#4",text="LOGIN ID",anchor=CENTER)
        self.tree_view.heading("#5",text="PASSWORD",anchor=CENTER)

        self.tree_view.bind('<Double-Button-1>',self.update_records)

        #connecting to database
        self.conn = sqlite3.connect('pathak_jii_database.db')
        # create cursor
        self.cursor = self.conn.cursor()
        #getting data from database
        self.cursor.execute("SELECT oid,* FROM details") #SELECT EVERYTHING FROM ADDRESSED TABLE WE CREATED ON CREATION OF DATABSE
        self.records = self.cursor.fetchall() #FETCHES DATA FROM DATABASE
        
        self.print_record = ""
        #LOOPING THRU FETCHED RECORD
        count = 0
        for record in self.records:
            #INSERTING DATA
            self.tree_view.insert(parent="",index="end",iid=count,values= (self.records[count][0],self.records[count][1],self.records[count][2],self.records[count][3],self.records[count][4]))
            count = count + 1

        #commit changes
        self.conn.commit()
        #close database
        self.conn.close()
        #Images for Buttons
        self.image3 = Image.open("search.png")
        self.search_button_image = ImageTk.PhotoImage(self.image3)

        self.image4 = Image.open("close_button.png")
        self.close_button_image = ImageTk.PhotoImage(self.image4)

        self.image5 = Image.open("add_button.png")
        self.add_button_image = ImageTk.PhotoImage(self.image5)

        self.image6 = Image.open("edit_button.png")
        self.edit_button_image = ImageTk.PhotoImage(self.image6)

        self.image7 = Image.open("delete_button.png")
        self.delete_button_image = ImageTk.PhotoImage(self.image7)

        #add button of tds view window
        self.gst_add_data_button = customtkinter.CTkButton(self.gst_view_frame2,text="",
                            command=lambda:self.add_gst_details(window_name ="add_gst_window",window_title="Add Party Details",inner_title="Add GST Login Details",need_buttons="yes"),
                            image=self.add_button_image,height=30,width=30)
        self.gst_add_data_button.grid(row=0,column=0,pady=(20,10),padx=(10,25))

        #search button of TDS Window
        self.gst_search_button = customtkinter.CTkButton(self.gst_view_frame2,text="",
                            image=self.search_button_image,height=25,width=30,
                            command=self.gst_record_search)
        self.gst_search_button.grid(row=0,column=1,pady=(20,10),padx=25)

        #Update_Record Button
        self.gst_update_record_button = customtkinter.CTkButton(self.gst_view_frame2,text="",
                                            image=self.edit_button_image,height=15,width=20,
                                            command=lambda: self.update_records(self))
        self.gst_update_record_button.grid(row=0,column=2,pady=(20,10),padx=25)

        #Delete Record Button
        self.gst_delete_record_button = customtkinter.CTkButton(self.gst_view_frame2,text="",
                                                 image= self.delete_button_image,height=10,width=20,
                                                 command=self.delete_record)
        self.gst_delete_record_button.grid(row=0,column=3,pady=(20,10),padx=(25,450))

        #close button of TDS Window
        self.gst_view_close_button = customtkinter.CTkButton(self.gst_view_frame2,text="",image=self.close_button_image,
                                                command=self.gst_window_close_button,height=30,width=20)
        self.gst_view_close_button.grid(row=0,column=4,pady=(20,10))

    
    #FUNCTION TO DELETE A RECORD   
    def delete_record(self):
        selected = self.tree_view.selection()
        if selected == ():
            messagebox.showinfo("Select Records","Please Select a Record to Delete !")
        else:
            messagebox.askokcancel("Delete Record","Are You Sure You Want To Delete this Record ?")
            value_list = self.tree_view.item(selected,'values')
            self.tree_view.delete(selected)
            conn = sqlite3.connect('pathak_jii_database.db')
            c = conn.cursor()
            c.execute("DELETE from details WHERE oid = " + value_list[0])
            conn.commit()
            conn.close()
            self.view_gst_records()
               

    def clear_fields(self):
        self.unique_id_entry.delete(0,END)
        self.gst_party_name_entry.delete(0,END)
        self.gst_id_entry.delete(0,END)
        self.gst_password_entry.delete(0,END)


    def add_gst_details(self,window_name,window_title,inner_title,need_buttons):
        global w_name
        w_name = window_name
        w_name = customtkinter.CTkToplevel(self)
        w_name.geometry("330x300")
        w_name.title(window_title)
    
        #heading label
        self.heading_label = customtkinter.CTkLabel(master= w_name, text=inner_title,bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=20,width=300)
        self.heading_label.grid(row=0,column=0,columnspan=8,padx=10,pady=10)
     
        #labels
        self.unique_id_label = customtkinter.CTkLabel(master= w_name, text="UNIQUE ID :",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=5,anchor="w",width=10,height=20)
        self.unique_id_label.grid(row=1,column=0,padx=2,pady=5,sticky=W)

        self.gst_party_name_label = customtkinter.CTkLabel(master= w_name, text="PARTY NAME :",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=5,anchor="w",width=10,height=20)
        self.gst_party_name_label.grid(row=2,column=0,padx=2,pady=5,sticky=W)
       
        self.gst_no_label = customtkinter.CTkLabel(master= w_name, text="GST NUMBER :",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=5,anchor="w",width=10,height=20)
        self.gst_no_label.grid(row=3,column=0,padx=2,pady=5,sticky=W)

        self.gst_id_label = customtkinter.CTkLabel(master= w_name, text="GST LOGIN ID :",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=5,anchor="w",width=10,height=20)
        self.gst_id_label.grid(row=4,column=0,padx=2,pady=5,sticky=W)

        self.gst_password_label = customtkinter.CTkLabel(master= w_name, text="PASSWORD : ",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#292929"),corner_radius=5,anchor="w",width=10,height=20)
        self.gst_password_label.grid(row=5,column=0,padx=2,pady=5,sticky=W)
        
        #entry fields
        self.unique_id_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="PLEASE KEEP IT BLANK",width=200,height=20)
        self.unique_id_entry.grid(row=1,column=1,sticky=W)

        self.gst_party_name_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="Party Name",width=200,height=20)
        self.gst_party_name_entry.grid(row=2,column=1,sticky=W)

        self.gst_no_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="Gst Number",width=200,height=20)
        self.gst_no_entry.grid(row=3,column=1,sticky=W)

        self.gst_id_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="GST ID",width=200,height=20)
        self.gst_id_entry.grid(row=4,column=1,sticky=W)

        self.gst_password_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="GST PASSWORD",width=200,height=20)
        self.gst_password_entry.grid(row=5,column=1,sticky=W)

        if need_buttons == "yes": 
            self.add_button = customtkinter.CTkButton(master=w_name, text="Add",command=self.add_data,width=80,hover_color=("blue","green"))
            self.add_button.grid(row=6,column=0,padx=5,pady=10,sticky=W)

            self.clear_fields_button = customtkinter.CTkButton(master=w_name, text="Clear Fields",command=self.clear_fields,width=80,hover_color=("blue","green"))
            self.clear_fields_button.grid(row=6,column=1,padx=5,pady=10,sticky=W)
        else:
            pass
    #
    def update_records(self,event):
        #get the current selection
        selected = self.tree_view.selection()
        if selected == ():
            messagebox.showwarning("Select a record","Please Select a Record or Double Click on record")
        else:
            self.add_gst_details(window_name="update_records",window_title="Update Records Window",inner_title="Update Records (GST)",need_buttons="no")
            #grab the values in current selection
            value_list = self.tree_view.item(selected,'values')
            self.unique_id_entry.insert(0,value_list[0])
            self.gst_party_name_entry.insert(0,value_list[1])
            self.gst_no_entry.insert(0,value_list[2])
            self.gst_id_entry.insert(0,value_list[3])
            self.gst_password_entry.insert(0,value_list[4])

            save_button = customtkinter.CTkButton(w_name,text="Save",command=self.save,width=80)
            save_button.grid(row=6,column=0,padx=5,pady=10)

    def save(self):
        #connecting to database
        self.conn = sqlite3.connect('pathak_jii_database.db')
        #create a cursor
        self.cursor = self.conn.cursor()
        # cursor.execute("CREATE TABLE details(party_name text,gst_no text,gst_id text,gst_password text)")
        self.cursor.execute("""UPDATE details SET 
        party_name = :pname,
        gst_no = :gst,
        gst_id = :gid,
        gst_password = :gpass
        WHERE oid = :oid""",
        {
            'pname':self.gst_party_name_entry.get(), 
            'gst':self.gst_no_entry.get(),
            'gid':self.gst_id_entry.get(),
            'gpass':self.gst_password_entry.get(),

            'oid':self.unique_id_entry.get()
            })
        #commit changes
        self.conn.commit()
        #close database
        self.conn.close()
        w_name.destroy()
        self.view_gst_records()

    #Search Function in gst
    def gst_record_search(self):
        self.gst_record_search_window = customtkinter.CTkToplevel(self)
        self.gst_record_search_window.geometry("320x200")
        self.gst_record_search_window.title("GST Search Window")

        self.search_box_var = customtkinter.StringVar(value="Search By")

        self.entry_box = customtkinter.CTkEntry(self.gst_record_search_window,placeholder_text="Enter Query",width=180)
        self.entry_box.grid(row=1,column=0,padx = 10,pady=20)

        self.search_box = customtkinter.CTkComboBox(self.gst_record_search_window,values=["Search By", "Party Name","GST No."],
                                     variable=self.search_box_var,width=100)
        self.search_box.grid(row=1,column=1,pady = 20)
        
        self.search_button = customtkinter.CTkButton(self.gst_record_search_window,text="Search",
                                    command=self.gst_record_search_func,width=60)
        self.search_button.grid(row=2,column=0)

    def gst_record_search_func(self):
        selected = self.search_box_var.get()
        searched = self.entry_box.get()
        self.gst_record_search_window.destroy()

        for record in self.tree_view.get_children():
                #clearing tree view
                self.tree_view.delete(record)

        conn = sqlite3.connect("Pathak_jii_database.db")
        cursor = conn.cursor()
        command=""
        if selected == "Party Name":
            command = "SELECT oid, * FROM tds_details WHERE party_name like ?"
        elif selected == "GST No.":
            command = "SELECT oid, * FROM tds_details WHERE gst_no like ?"
        elif searched == "Search By":
            pass
        gst_records = cursor.execute(command,(searched,))
        gst_records = cursor.fetchall()   
        
        count = 0
        for record in gst_records:
            self.tree_view.insert(parent="",index="end",iid=count,values= (gst_records[count][0],gst_records[count][1],gst_records[count][2],gst_records[count][3],gst_records[count][4],gst_records[count][5]))
            count+=1
        conn.commit()
        conn.close()        


#for tds
    def create_tds_database(self):
        #creating database
        conn = sqlite3.connect('pathak_jii_database.db')
        # #create a cursor
        cursor = conn.cursor()
        # #create a table just one time
        cursor.execute("CREATE TABLE IF NOT EXISTS tds_details (party_name text,pan_no text,tan_no text,login_id text,tds_password text,filling_status text)")
        #commit changes
        conn.commit()
        # #close database
        conn.close()


    def create_tree_view(self):
        self.gst_view_frame2.destroy()
        self.tds_tree_view_frame.destroy()
        self.tree_view_frame.destroy()
        self.tds_tree_view_frame2.destroy()

        # TDS SEARCH,CLOSE BUTTON FRAME
        self.tds_tree_view_frame2 = customtkinter.CTkFrame(master=self,height=50)
        self.tds_tree_view_frame2.pack(side=TOP,anchor="n",fill=X)

        self.tds_tree_view_frame = customtkinter.CTkFrame(master=self,fg_color="white",bg_color="white")
        self.tds_tree_view_frame.pack(fill=BOTH,anchor = "n")

        #styling tree
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="D3D3D3",
                            foreground="BLACK",
                            rowheight=25,
                            fieldbackground="#D3D3D3")
        #create treeview frame
        #add a scroll bar
        tds_tree_scroll = Scrollbar(self.tds_tree_view_frame)
        tds_tree_scroll.pack(side=RIGHT, fill=Y)

        #create treeview
        self.tds_tree_view = ttk.Treeview(self.tds_tree_view_frame,yscrollcommand=tds_tree_scroll.set)
        self.tds_tree_view.pack(fill=BOTH)
        #Configure the scrollbar
        tds_tree_scroll.config(command=self.tds_tree_view.yview)
        #define treeview column
        self.tds_tree_view['columns'] = ('RECORD ID','PARTY NAME','PAN NO.','TAN NO.','LOGIN ID','PASSWORD','FILLING_STATUS')
        #formate our columns
        self.tds_tree_view.column("#0",width=0,anchor=CENTER,stretch=NO)
        self.tds_tree_view.column("RECORD ID",width=45,anchor=CENTER)
        self.tds_tree_view.column("PARTY NAME",anchor=CENTER,width=120)
        self.tds_tree_view.column("PAN NO.",anchor=CENTER,width=105)
        self.tds_tree_view.column("TAN NO.",anchor=CENTER,width=80)
        self.tds_tree_view.column("LOGIN ID",anchor=CENTER,width=80)
        self.tds_tree_view.column("PASSWORD",anchor=CENTER,width=80)
        self.tds_tree_view.column("FILLING_STATUS",anchor=CENTER,width=80)
 
        #giving column headings
        self.tds_tree_view.heading("#0",text="",anchor=W)
        self.tds_tree_view.heading("#1",text="RECORD ID",anchor=W)
        self.tds_tree_view.heading("#2",text="PARTY NAME",anchor=CENTER)
        self.tds_tree_view.heading("#3",text="PAN NO.",anchor=CENTER)
        self.tds_tree_view.heading("#4",text="TAN NO.",anchor=CENTER)
        self.tds_tree_view.heading("#5",text="LOGIN ID",anchor=CENTER)
        self.tds_tree_view.heading("#6",text="PASSWORD",anchor=CENTER)
        self.tds_tree_view.heading("#7",text="FILLING STATUS",anchor=CENTER)

        self.tds_tree_view.bind('<Double-Button-1>',self.tds_update_records)

        self.create_tds_database()
        #connecting to database
        conn = sqlite3.connect('pathak_jii_database.db')
        # create cursor
        cursor = conn.cursor()
        #getting data from database
        cursor.execute("SELECT oid,* FROM tds_details") 
        tds_records = cursor.fetchall() 
        #LOOPING THRU FETCHED RECORD
        count = 0
        for record in tds_records:
            #INSERTING DATA
            self.tds_tree_view.insert(parent="",index="end",iid=count,values= (tds_records[count][0],tds_records[count][1],tds_records[count][2],tds_records[count][3],tds_records[count][4],tds_records[count][5],tds_records[count][6]))
            count = count + 1
        

        #commit changes
        conn.commit()
        #close database
        conn.close()
        #Images for Buttons
        self.image3 = Image.open("search.png")
        self.search_button_image = ImageTk.PhotoImage(self.image3)

        self.image4 = Image.open("close_button.png")
        self.close_button_image = ImageTk.PhotoImage(self.image4)

        self.image5 = Image.open("add_button.png")
        self.add_button_image = ImageTk.PhotoImage(self.image5)

        self.image6 = Image.open("edit_button.png")
        self.edit_button_image = ImageTk.PhotoImage(self.image6)

        self.image7 = Image.open("delete_button.png")
        self.delete_button_image = ImageTk.PhotoImage(self.image7)

        #add button of tds view window
        self.add_data_button = customtkinter.CTkButton(self.tds_tree_view_frame2,text="",
                            command=lambda:self.add_tds_details_window(window_name="add_tds_details",window_title="Add TDS Details",inner_title="ADD TDS DETAILS",need_buttons="yes"),
                            image=self.add_button_image,height=30,width=30)
        self.add_data_button.grid(row=0,column=0,pady=(20,10),padx=(10,25))
        
        #search button of TDS Window
        self.tds_search_button = customtkinter.CTkButton(self.tds_tree_view_frame2,text="",
                            image=self.search_button_image,height=25,width=30,
                            command=self.tds_record_search)
        self.tds_search_button.grid(row=0,column=1,pady=(20,10),padx=25)
        #Update_Record Button
        update_record_button = customtkinter.CTkButton(self.tds_tree_view_frame2,text="",
                                            command= lambda: self.tds_update_records(self),
                                            image=self.edit_button_image,height=15,width=20)
        update_record_button.grid(row=0,column=2,pady=(20,10),padx=25)
        #Delete Record Button
        delete_record_button = customtkinter.CTkButton(self.tds_tree_view_frame2,text="",
                                                command= self.tds_delete_record,image=self.delete_button_image,
                                                height=10,width=20)
        delete_record_button.grid(row=0,column=3,pady=(20,10),padx=(25,450))
        #close button of TDS Window
        self.tds_close_button = customtkinter.CTkButton(self.tds_tree_view_frame2,text="",image=self.close_button_image,
                                                height=30,width=20,command=self.tds_window_close_button)
        self.tds_close_button.grid(row=0,column=4,pady=(20,10))
        

    def add_tds_details_window(self,window_name,window_title,inner_title,need_buttons):
        global w_name
        w_name = window_name
        w_name = customtkinter.CTkToplevel(self)
        w_name.geometry("330x300")
        w_name.title(window_title)
    
        #heading label
        heading_label = customtkinter.CTkLabel(master= w_name, text=inner_title,bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=20,width=300)
        heading_label.grid(row=0,column=0,columnspan=8,padx=10,pady=10)
     
        #labels
        unique_id_label1 = customtkinter.CTkLabel(master= w_name, text="UNIQUE ID :",bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        unique_id_label1.grid(row=1,column=0,padx=2,pady=5,sticky=W)

        tds_party_name_label = customtkinter.CTkLabel(master= w_name, text="PARTY NAME :",bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        tds_party_name_label.grid(row=2,column=0,padx=2,pady=5,sticky=W)
       
        pan_no_label = customtkinter.CTkLabel(master= w_name, text="PAN NUMBER :",bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        pan_no_label.grid(row=3,column=0,padx=2,pady=5,sticky=W)

        tan_no_label = customtkinter.CTkLabel(master= w_name, text="TAN NUMBER :",bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        tan_no_label.grid(row=4,column=0,padx=2,pady=5,sticky=W)

        tds_id_label = customtkinter.CTkLabel(master= w_name, text="TDS LOGIN ID :",bg_color=("#FFFFFF", "#292929"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        tds_id_label.grid(row=5,column=0,padx=2,pady=5,sticky=W)

        tds_password_label = customtkinter.CTkLabel(master= w_name, text="PASSWORD : ",bg_color=("#FFFFFF", "#3A3B3C"),fg_color=("#FFFFFF", "#3A3B3C"),corner_radius=5,anchor="w",width=10,height=20)
        tds_password_label.grid(row=6,column=0,padx=2,pady=5,sticky=W)
        
        #entry fields
        self.unique_id_label = customtkinter.CTkLabel(master=w_name,text="Auto Generated",width=200,height=20,anchor="w")
        self.unique_id_label.grid(row=1,column=1,sticky=W)

        self.party_name_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="Party Name",width=200,height=20)
        self.party_name_entry.grid(row=2,column=1,sticky=W)

        self.pan_no_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="Pan Number",width=200,height=20)
        self.pan_no_entry.grid(row=3,column=1,sticky=W)

        self.tan_no_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="Tan Number",width=200,height=20)
        self.tan_no_entry.grid(row=4,column=1,sticky=W)

        self.tds_id_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="TDS ID",width=200,height=20)
        self.tds_id_entry.grid(row=5,column=1,sticky=W)

        self.tds_password_entry = customtkinter.CTkEntry(master=w_name, placeholder_text="TDS Password",width=200,height=20)
        self.tds_password_entry.grid(row=6,column=1,sticky=W)
        #buttons
        if need_buttons == "yes": 
            add_button = customtkinter.CTkButton(master=w_name, text="Add",width=80,hover_color=("blue","green"),command=self.add_tds_details)
            add_button.grid(row=7,column=0,padx=10,pady=10,sticky=W)

            # clear_fields_button = customtkinter.CTkButton(master=w_name, text="Clear Fields",width=80,hover_color=("blue","green"),command=self.tds_clear_fields)
            # clear_fields_button.grid(row=8,column=1,padx=5,pady=10,sticky=W)
        else:
            pass

    def add_tds_details(self):
        #connecting to database
        conn = sqlite3.connect('pathak_jii_database.db')
        #create a cursor
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tds_details VALUES (:party_name,:pan_no,:tan_no,:tds_id,:tds_password,:filling_status)", 
        {
            'party_name':self.party_name_entry.get(), 
            'pan_no':self.pan_no_entry.get(),
            'tan_no':self.tan_no_entry.get(),
            'tds_id':self.tds_id_entry.get(),
            'tds_password':self.tds_password_entry.get(),
            'filling_status':"None"
        })
        # party_name text,pan_no text,tan_no text,login_id text,tds_password text,filling_status text
        #commit changes
        conn.commit()
        #close database
        conn.close()
        # clear_fields()
        w_name.destroy()
        self.create_tree_view()
            
    def tds_update_records(self,event):
        # w_name.destroy()
        #get the current selection
        selected = self.tds_tree_view.selection()
        if selected == ():
            messagebox.showwarning("Select a record","Please Select a Record or Double Click on record")
        else:
            self.add_tds_details_window(window_name="update_tds_records",window_title="Update TDS Records",inner_title="Update Records (TDS)",need_buttons="no")
            #grab the values in current selection
            global value_list
            value_list = self.tds_tree_view.item(selected,'values')
            
            self.unique_id_label.configure(text=value_list[0])
            self.party_name_entry.insert(0,value_list[1])
            self.pan_no_entry.insert(0,value_list[2])
            self.tan_no_entry.insert(0,value_list[3])
            self.tds_id_entry.insert(0,value_list[4])
            self.tds_password_entry.insert(0,value_list[5])

            save_button = customtkinter.CTkButton(w_name,text="Save",command=self.tds_save,width=80)
            save_button.grid(row=7,column=0,padx=5,pady=10)

    def tds_save(self):
        #connecting to database
        conn = sqlite3.connect('pathak_jii_database.db')
        #create a cursor
        cursor = conn.cursor()
        # party_name text,pan_no text,tan_no text,login_id text,tds_password text,filling_status text
        cursor.execute("""UPDATE tds_details SET 
        party_name = :pname,
        pan_no = :pan,
        tan_no = :tan,
        login_id = :login,
        tds_password = :tpass
        WHERE oid = :oid""",
        {
            'pname':self.party_name_entry.get(), 
            'pan':self.pan_no_entry.get(),
            'tan':self.tan_no_entry.get(),
            'login':self.tds_id_entry.get(),
            'tpass':self.tds_password_entry.get(),

            'oid':value_list[0]
            })
        #commit changes
        conn.commit()
        #close database
        conn.close()
        w_name.destroy()
        self.create_tree_view()

    def tds_delete_record(self):
        selected = self.tds_tree_view.selection()
        if selected == ():
            messagebox.showinfo("Select Record !","Please Select a Record from the list !")
        else:
            messagebox.askokcancel("Delete Record","Are You Sure You Want To Delete this Record ?")
            value_list = self.tds_tree_view.item(selected,'values')
            self.tds_tree_view.delete(selected)
            conn = sqlite3.connect('pathak_jii_database.db')
            c = conn.cursor()
            c.execute("DELETE from tds_details WHERE oid = " + value_list[0])
            conn.commit()
            conn.close()
            self.create_tree_view()  

    def tds_window_close_button(self):
        self.tds_tree_view_frame2.destroy()
        self.tds_tree_view_frame.destroy()

    #Function Search in TDS
    def tds_record_search(self):
        self.tds_record_search_window = customtkinter.CTkToplevel(self)
        self.tds_record_search_window.geometry("320x200")
        self.tds_record_search_window.title("TDS Search Window")

        self.search_box_var = customtkinter.StringVar(value="Search By")

        self.entry_box = customtkinter.CTkEntry(self.tds_record_search_window,placeholder_text="Enter Query",width=180)
        self.entry_box.grid(row=1,column=0,padx = 10,pady=20)

        self.search_box = customtkinter.CTkComboBox(self.tds_record_search_window,values=["Search By", "Party Name","Pan No."],
                                     variable=self.search_box_var,width=100)
        self.search_box.grid(row=1,column=1,pady = 20)
        
        self.search_button = customtkinter.CTkButton(self.tds_record_search_window,text="Search",
                                    command=self.tds_record_search_func,width=60)
        self.search_button.grid(row=2,column=0)

    def tds_record_search_func(self):
        selected = self.search_box_var.get()
        searched = self.entry_box.get()
        self.tds_record_search_window.destroy()

        for record in self.tds_tree_view.get_children():
                #clearing tree view
                self.tds_tree_view.delete(record)

        conn = sqlite3.connect("Pathak_jii_database.db")
        cursor = conn.cursor()
        command=""
        if selected == "Party Name":
            command = "SELECT oid, * FROM tds_details WHERE party_name like ?"
        elif selected == "Pan No.":
            command = "SELECT oid, * FROM tds_details WHERE pan_no like ?"
        elif searched == "Search By":
            pass
        tds_records = cursor.execute(command,(searched,))
        tds_records = cursor.fetchall()   
        
        count = 0
        for record in tds_records:
            self.tds_tree_view.insert(parent="",index="end",iid=count,values= (tds_records[count][0],tds_records[count][1],tds_records[count][2],tds_records[count][3],tds_records[count][4],tds_records[count][5]))
            count+=1
        conn.commit()
        conn.close()



#DRIVER CODE
if __name__ == "__main__":
    app = Record_App()
    app.mainloop() 
    

    #creating database
    # conn = sqlite3.connect('pathak_jii_database.db')
    # #create a cursor
    # cursor = conn.cursor()
    # #create a table just one time
    # cursor.execute("CREATE TABLE details(party_name text,gst_no text,gst_id text,gst_password text)")
    # #commit changes
    # conn.commit()
    # #close database
    # conn.close()
