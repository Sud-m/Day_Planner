from tkinter import * #GUI
from tkinter import ttk #Displays message box to enter stuff (To enter user and pass)
from tkinter import messagebox #To display message as a pop up box
from tkinter import scrolledtext #Provides a scrollbar to text box
from datetime import date #To enter the date
from datetime import datetime 
from math import ceil #REturns ceiling value of a number (eg: ceil(201.1)=202)
import matplotlib.pyplot as plt #For graphs, plt for easier calling
import numpy as np #To compute multidimensional arrays
from PIL import Image, ImageTk #To import and display images (for the buttons)
import time #Functions for working with time
import mysql.connector
from mysql.connector import Error
stakk=[]

def retrieve_data(): #
    with open('data.txt','r') as f:
        data = f.read().split(r"%%//%%")[:-1]
    data = [eval(task) for task in data]
    return data
with open('date.txt','r') as f:
    cont = eval(f.read().strip().split("\n")[1]) #The strip() method removes characters from both left and right
    d = f.read().strip().split("\n")[0]          #based on the argument (a string specifying the set of characters to be removed).

def stackapend(a,b,c,d):
        connection = mysql.connector.connect(host='localhost',
                                         database='hello',
                                         user='root',
                                         password='root')
        
        mySql_insert_query = """INSERT INTO sudhanva (Name,Info,Date,Time) 
                           VALUES (%s,%s,%s,%s) """

        records_to_insert = [(a,b,c,d)]
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.execute("select * from sudhanva;")
        myresult=cursor.fetchall()
        for x in myresult:
            stakk.append(x)

def normalstack():
    wnd=Tk()
    wnd.geometry("400x800+100+20")
    wnd.config(bg="black")
    wnd.title("History of current session.")
    wnd.iconbitmap('history.png')
    Label(wnd,text="History",font=('Calistoga',20,"bold"),bg="black",fg="white").pack()
    Label(wnd,text="\n",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()
    for i in range(len(stakk)-1,-1,-1):
        Label(wnd,text=((len(stakk)-i),".",(''.join(map(str, stakk[i][0])))),font=('Calistoga',10,"bold"),bg="black",fg="white").pack()
        Label(wnd,text="\n",font=('Calistoga',5,"bold underline"),bg="black",fg="white").pack()
    
class Encryption:
    def __init__(self,data):
        self.data = data
        
    def encrypt(self,letters):
        data = list(self.data)
        encrypted = ''
        for i in range(len(data)):
            if data[i].isalpha():
                if data[i].isupper():
                    data[i] = letters[25-letters.index(data[i])].lower()
                else:
                    data[i] = letters[25-letters.index(data[i].upper())]
            elif data[i].isdigit:
                (data[i]) = 9 - int(data[i])
        for i in data:
            encrypted += str(i)
        return(encrypted)
        
    def decrypt(self,letters):
        data = list(self.data)
        decrypted = ''
        for i in range(len(data)):
            if data[i].isalpha():
                if data[i].isupper():
                    data[i] = letters[25-letters.index(data[i])].lower()
                else:
                    data[i] = letters[25-letters.index(data[i].upper())]
            elif data[i].isdigit:
                 (data[i]) = 9 - int(data[i])
        for i in data:
            decrypted += str(i)
        return(decrypted)

def date_conversion(date):
    date = date.split("-")
    month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

    mon=date[1]
    if int(date[2]) in [1,21,31]:
        date[2] = str(date[2]) + "st"
    elif int(date[2]) in [2,22]:
        date[2] = str(date[2]) + "nd"
    elif int(date[2]) in [3,23]:
        date[2] = str(date[2]) + "rd"
    elif int(date[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
        date[2] = str(date[2]) + "th"
    return "{} {}, {}".format(date[2],month[int(mon)],str(date[0]))

def get_todays_events(pk):
    date = datetime.today().strftime(r'%Y-%m-%d')
    data = retrieve_data()
    cont = data[pk]["data"] 
    tasks = []
    for dic in cont:
        pub_date = dic["date"]
        if pub_date==date:
            tasks.append(dic)
    return tasks

def graph_display(pk):
    wnd = Tk()
    
    wnd.geometry("400x200+150+150")
    wnd.config(bg="#A9DFBF")
    wnd.title("Select Range Of Dates")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="Select A Date",font=('Calistoga',20,"bold"),bg="#A9DFBF",fg="#515A5A").pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    startDateEntry = ttk.Entry(wnd,font=('Calistoga',20,"bold"))
    startDateEntry.pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    def graphing(pk):
        s_date = startDateEntry.get() #2020-10-10
        wnd.destroy()
        if len(s_date.split("-")[0])!=4 or len(s_date.split("-")[1])!=2 or len(s_date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                graph_display(pk)
                
        dates = []
        for i in range(0, 6):
            base = s_date.split("-")[:2]
            add = int(s_date.split("-")[2])-i
            if len(str(add))==1:
                add = "0"+str(add)
            base.append(str(add))
            st=""
            for s in base:
                st+=s
                if base.index(s)!=2:
                    st+="-"
            dates.append(st)

        x = np.arange(6)
        data = retrieve_data()
        tasks = data[pk]["data"]
        matched_dates = []
        for task in tasks:
            if task["date"] in dates:
                matched_dates.append([task["date"],task["status"]])
        req_counts, req_confirmed_counts = [0,0,0,0,0,0],[0,0,0,0,0,0]
        for k in matched_dates:
            if k[1]=="Yes":
                req_confirmed_counts[dates.index(k[0])]+=1

            req_counts[dates.index(k[0])] += 1
            
        #req_counts--> Today, Yesterday,...

        plt.plot(x,req_counts,'bo',ls="solid",markersize=5,markeredgecolor="red",label="Total Tasks")
        plt.plot(x,req_confirmed_counts,'yo',ls='solid',markersize=5,markeredgecolor="green",label="Completed Tasks")
        plt.xticks(x,dates)
        plt.xlabel("Last Six Days")
        plt.ylabel("No. of Tasks")
        plt.title("Productivity Statistics")
        plt.legend(loc="upper right")
        plt.show()
        
    Button(wnd,text="SUBMIT",bg="#D98880",fg="white",font=('Calistoga',20,"bold"),command=lambda var=pk: graphing(var)).pack()

    wnd.mainloop()


def old_homepage(pk,date=d,tasks=cont[:2]):
    wnd = Toplevel()#Toplevel widgets work as windows that are directly managed by the window manager.
    #They do not necessarily have a parent widget on top of them.
    wnd.attributes("-fullscreen", True)
    wnd.configure(bg="#07EABD")#background colour
    wnd.bind("<Escape>", lambda event: wnd.attributes("-fullscreen", False))#Lambda uses this parameter to pass in event data to the handler. This parameter is usually of the Python dict type. It can also be list, str, int, float, or NoneType type.
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')#iconbitmap(bitmap) sets the icon of the window/frame widget to bitmap . The bitmap must be an ico type, but not png or jpg type, otherwise, the image will not display
    #as the icon. The above image shows when the ico type is used in iconbitmap

    title_frame = Frame(wnd,bg="#07EABD")#w = Frame ( master-parent window, option, ... )
    for i in range(3):
        Label(title_frame,text="\t\t\t\t\t\t\t", bg="#07EABD").grid(row=0,column=i,pady=5)#The Grid geometry manager puts the widgets in a 2-dimensional table. The master widget is split into a number of rows and columns, and each “cell” in the resulting table can hold a widget.
    #table,Lable used to display text or an image 
    title_font = ('Calistoga',40,"bold")
    current_date_viewed = Label(title_frame,text="Viewing: "+date_conversion(date),font=('Calistoga',20,"bold"),bg="#07EABD",fg="black")#display of date of the calander being viewed
    current_date_viewed.grid(row=1,column=0)

    title = Label(title_frame,text=" Day Planner",font=('Calistoga',40,"bold underline"),bg="#07EABD",fg="black")
    title.grid(row=1,column=1)

    def destroy():
        wnd.destroy()#It is useful in controlling the behavior of various widgets which depend on each other. Also when a process is complete by some user action we need to destroy the GUI components to free the memory as well as clear the screen
    back = PhotoImage(master=wnd,file="exit.png")#function returns the image object, only supports GIF and PGM/PPM formats
    back_button = Button(wnd, command=destroy)#calls destroy
    back_button.config(image=back)#sets image as back
    back_button.grid(row=1,column=2)

    Label(title_frame,text="\n",bg="#07EABD").grid(row=2,columnspan=3)
    
    title_frame.grid(row=0,columnspan=3,padx=50)
    Label(wnd,text=" ",bg="#07EABD").grid(row=1,columnspan=3)
    #inside today
    #Profile Panel
    profile_pane = Frame(wnd,bg="#07EABD",borderwidth=4,relief=RAISED)
    profile_font = ('Calistoga',20,"bold")
    data = retrieve_data()
    name = Label(profile_pane,text=data[pk]["name"],font=profile_font,bg="#07EABD",fg="black")
    name.grid(row=0,column=0)
    time = Label(profile_pane,text=str(datetime.time(datetime.now())).split(".")[0],font=profile_font,bg="#07EABD",fg="black")
    time.grid(row=1,column=0)#current time/date from datetime function
    date_ = Label(profile_pane,text=date_conversion(datetime.today().strftime(r'%Y-%m-%d')),font=profile_font,bg="#07EABD",fg="black")
    date_.grid(row=2,column=0)
    day = Label(profile_pane,text=datetime.today().strftime("%A"),font=profile_font,bg="#07EABD",fg="black")
    day.grid(row=3,column=0)
    profile_pane.grid(row=2,column=0,pady=15)  #pady,padx are spacing  

    Label(wnd,bg="#07EABD",text=" ").grid(row=3,column=0)
    Label(wnd,bg="#07EABD",text="\n\n").grid(row=4,column=0)

    profile_pane_down = Frame(wnd,bg="#07EABD",borderwidth=4,relief=RAISED)

    if date==datetime.today().strftime(r'%Y-%m-%d'):
        text = "You Have {} \n Tasks/Events Planned\n Today.".format(len(tasks))
    elif date>datetime.today().strftime(r'%Y-%m-%d'):
        text = "You Have {} \n Tasks/Events Planned\nOn {}.".format(len(tasks),date_conversion(date))
    else:
        text = "You Had {} \n Tasks/Events Planned\n On {}.".format(len(tasks),date_conversion(date))
    reminder = Label(profile_pane_down,text=text,font=profile_font,bg="#07EABD",fg="black")
    reminder.grid(row=1,column=0)
    profile_pane_down.grid(row=5,column=0)

    #TASKS PANEL
    def tasks_display(tasks):
        task_panel = Frame(wnd,bg="#07EABD",borderwidth=2,relief="solid")
        Label(task_panel,text="\tYour Tasks\t",bg="#07EABD",fg="black",font=("Heletivca",25,"bold")).grid(row=0,column=0)
        
        task_font = ("Heletivca",15,"bold")
        task_info_font = ("Heletivca",18,"bold")
        task_number_font = ("Times",20,"bold")
        cur=1
        for task in tasks:
            taskwise_panel = Frame(task_panel,bg="#07EABD",borderwidth=4,relief="solid")
            Label(taskwise_panel,text="Task {}".format(data[pk]["data"].index(task)+1),bg="#07EABD",font=task_number_font,fg="black").grid(row=0,column=0)
            task_name = Label(taskwise_panel,text=task["task_name"],bg="#07EABD",fg="black",font=("Heletivca",25,"bold underline"))
            task_name.grid(row=1,column=0)
            
            length = len(task["task"])
            original = task["task"]
            final = ""
            if length>25:
                while length>25:
                    if length>50:
                        final += task["task"][:25]+"\n"
                        task["task"] = task["task"][25:]
                        length-=25
                    else:
                        final += task["task"][:25]
                        task["task"] = task["task"][25:]
                        length-=25
            else:
                final=task["task"]
            task["task"] = original
                
            task_info = Label(taskwise_panel,text=final,bg="#07EABD",fg="black",font=task_info_font)
            task_info.grid(row=2,column=0)
            task_date = Label(taskwise_panel,text=date_conversion(task["date"]),bg="#07EABD",fg="black",font=task_font)
            task_date.grid(row=3,column=0)
            task_time = Label(taskwise_panel,text=task["time"],bg="#07EABD",fg="black",font=task_font)
            task_time.grid(row=4,column=0)
            taskwise_panel.grid(row=cur,column=0,pady=10)
            cur+=1

        task_panel.grid(row=1,column=1,rowspan=10)
    tasks_display(tasks)

    buttons_frame = Frame(wnd,bg="#07EABD")

    Label(buttons_frame,text="\n\n",bg="#07EABD").grid(row=1,column=0)
    change_date_img = PhotoImage(master=wnd,file='calendar.png')
    change_date = Button(buttons_frame,command=lambda var=pk: date_selection(var))
    change_date.config(image=change_date_img)
    change_date.grid(row=2,column=0)

    buttons_frame.grid(row=1,column=2,rowspan=10)
    wnd.mainloop()

def add_task(pk):
    wnd = Tk()#activates tkinter
    wnd.geometry("400x800+150+20")
    wnd.config(bg="black")
    wnd.title("Add Task!")
    wnd.iconbitmap('logo.ico')#for adding tasks

    Label(wnd,text="Add A New Task Here",font=('Calistoga',20,"bold"),bg="black",fg="white").pack()
    #.pack() - geometry manager organizes widgets in blocks before placing them in the parent widget
    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    name = Label(wnd,text="Task Name",font=('Calistoga',20,"bold"),bg="black",fg="white")
    name.pack()
    nameEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    #Entry widget is used to accept single-line text strings from a user (input)
    nameEntry.insert(0,'Homework')
    nameEntry.pack()

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()
    info = Label(wnd,text="Task Information",font=('Calistoga',20,"bold"),bg="black",fg="white")
    info.pack()
    infoEntry = scrolledtext.ScrolledText(
        master = wnd,
        wrap   = WORD,
        width  = 25,
        height = 5)

    infoEntry.pack(padx=10, pady=10, fill=BOTH)
    infoEntry.insert(INSERT,"Enter Task Information here...")
    infoEntry.config(font=('Calistoga',15))

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    date = Label(wnd,text="Date of Task",font=('Calistoga',20,"bold"),bg="black",fg="white")
    date.pack()
    dateEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    dateEntry.insert(0,'2020-1-1')#used to enter values into the window
    dateEntry.pack()

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    time = Label(wnd,text="Time of Task",font=('Calistoga',20,"bold"),bg="black",fg="white")
    time.pack()
    timeEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    timeEntry.insert(0,'23:59')
    timeEntry.pack()
    
    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()
    def adding_task():
        #It is used to get the text written inside the widge
        name = nameEntry.get()
        info = infoEntry.get(1.0,END)
        date = dateEntry.get()
        time = timeEntry.get()

        def check(date, time):
            if len(date.split("-")[0])!=4 or len(date.split("-")[1])!=2 or len(date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                add_task(pk)
            if len(time.split(":")[0])!=2 or len(time.split(":")[1])!=2:
                messagebox.showerror('Invalid Time.','Enter a Valid Time of Day')
                add_task(pk)

        if len(name)==0 or len(info)==0 or len(date)==0 or len(time)==0:
            messagebox.showerror("Invalid Entries.","Kindly Re-Enter or Ensured that All Fields are Filled.")
            add_task(pk)

        check(date,time)
        
        if date<datetime.today().strftime(r'%Y-%m-%d'):
            messagebox.showerror('Invalid Date.','Enter a Valid Date')
            add_task(pk)
        elif date==datetime.today().strftime(r'%Y-%m-%d') and time<str(datetime.time(datetime.now())).split(".")[0]:
            messagebox.showerror('Invalid Time.','Enter a Valid Time of Day')
            add_task(pk)
        else:
            stackapend(name,info,date,time)
            
            data = retrieve_data()
            data[pk]["data"].append(
                {
                    "task_name":name,
                    "id": str(int(data[pk]["data"][-1]["id"])+1),
                    "task":info,
                    "date":date,
                    "time":time,
                    "status":"No"
                }
            )

            with open("data.txt","r+") as f:
                cont = f.read()
                base = eval(cont.split(r"%%//%%")[pk])
                base["data"] = data[pk]["data"]
                l = cont.split(r"%%//%%")
                l[pk] = str(base)
                for i in range(len(l)-1):
                    if i!=pk:
                        l[i]=str(eval(l[i]))
        
            with open('data.txt','w') as f:
                pass

            for user in l[:-1]:
                with open("data.txt","a") as f:
                    f.write(user.strip())
                    f.write("\n%%//%%\n")

            wnd.destroy()
            messagebox.showinfo("Success!","Task '{}' has been successfully added!".format(name))

    submit = Button(wnd,text="ADD TASK",bg="#B54A35",font=('Calistoga',15,"bold"),fg="white",command=adding_task,relief="groove")
    submit.pack()
    wnd.mainloop()

def date_selection(pk):
    wnd = Tk()
    wnd.geometry("400x200+150+150")
    wnd.config(bg="#A9DFBF")
    wnd.title("Select A Date")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="Select A Date",font=('Calistoga',20,"bold"),bg="#A9DFBF",fg="#515A5A").pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    dateselectionEntry = ttk.Entry(wnd,font=('Calistoga',20,"bold"))
    dateselectionEntry.pack()

    Label(wnd,text="",bg="#A9DFBF").pack()

    def select_date():
        date = dateselectionEntry.get()#2020-10-10
        wnd.destroy()

        if len(date.split("-")[0])!=4 or len(date.split("-")[1])!=2 or len(date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                date_selection(pk)

        data = retrieve_data()

        cont = data[pk]["data"]
        tasks = []
        for dic in cont:
            pub_date = dic["date"]
            if pub_date==date:
                tasks.append(dic)

        with open('date.txt','w') as f:
            f.write(date + "\n")
            f.write(str(tasks))
        
        old_homepage(pk,date=date,tasks=tasks)

    submit = Button(wnd,text="SUBMIT",bg="#D98880",fg="white",font=('Calistoga',20,"bold"),command=select_date)
    submit.pack()
    wnd.mainloop()

    
def homepage(pk):
    wnd = Tk()
    wnd.attributes("-fullscreen", True)
    wnd.configure(bg="#07EABD")
    wnd.bind("<Escape>", lambda event: wnd.attributes("-fullscreen", False))
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')

    title_frame = Frame(wnd,bg="#07EABD")
    for i in range(3):
        Label(title_frame,text="\t\t\t\t\t\t\t", bg="#07EABD").grid(row=0,column=i,pady=5)
    title_font = ('Calistoga',40,"bold")
    with open('date.txt','r') as f:
        date = f.read().strip().split("\n")[0]
    
    def today_view():
        old_homepage(pk,date=datetime.today().strftime(r'%Y-%m-%d'),tasks=get_todays_events(pk))

    today = Button(wnd,text="Today",font=('Calistoga',20,"bold"),bg="#FF2A00",fg="white",command=today_view,width=15)
    today.grid(row=1,column=0)

    title = Label(title_frame,text=" Day Planner",font=('Calistoga',40,"bold underline"),bg="#07EABD",fg="black")
    title.grid(row=1,column=1)

    close_img = PhotoImage(master=wnd,file="close.png")
    close = Button(wnd,command=lambda cur=wnd: login(cur),relief="groove")
    close.config(image=close_img)
    close.grid(row=1,column=2)

    

    Label(title_frame,text="\n",bg="#07EABD").grid(row=9,columnspan=3)
    
    title_frame.grid(row=0,columnspan=3,padx=50)
    Label(wnd,text=" ",bg="#07EABD").grid(row=1,columnspan=3)
    
    #Profile Panel
    profile_pane = Frame(wnd,bg="#07EABD",borderwidth=4,relief="groove")
    profile_font = ('Calistoga',20,"bold")
    data = retrieve_data()
    name = Label(profile_pane,text=data[pk]["name"],font=profile_font,bg="#07EABD",fg="black")
    name.grid(row=0,column=0)
    time = Label(profile_pane,text=str(datetime.time(datetime.now())).split(".")[0],font=profile_font,bg="#07EABD",fg="black")
    time.grid(row=1,column=0)
    date = Label(profile_pane,text=date_conversion(datetime.today().strftime(r'%Y-%m-%d')),font=profile_font,bg="#07EABD",fg="black")
    date.grid(row=2,column=0)
    day = Label(profile_pane,text=datetime.today().strftime("%A"),font=profile_font,bg="#07EABD",fg="black")
    day.grid(row=3,column=0)
    profile_pane.grid(row=2,column=0,pady=15)    

    Label(wnd,bg="#07EABD",text=" ").grid(row=3,column=0)
    Label(wnd,bg="#07EABD",text="\n\n").grid(row=4,column=0)

    profile_pane_down = Frame(wnd,bg="#07EABD",borderwidth=4,relief="groove")
    text = "You Have/Had {} \n Tasks/Events Planned.".format(len(data[pk]["data"]))
    reminder = Label(profile_pane_down,text=text,font=profile_font,bg="#07EABD",fg="black")
    reminder.grid(row=1,column=0)
    profile_pane_down.grid(row=5,column=0)

    #TASKS PANEL
    def tasks_display(tasks):
        task_panel = Frame(wnd,bg="#07EABD",borderwidth=2,relief="solid")
        Label(task_panel,text="\tYour Tasks\t",bg="#07EABD",fg="black",font=("Heletivca",25,"bold")).grid(row=0,column=0)
        
        task_font = ("Heletivca",15,"bold")
        task_info_font = ("Heletivca",16,"bold")
        task_number_font = ("Times",20,"bold")
        cur=1
        for task in tasks:
            taskwise_panel = Frame(task_panel,bg="#07EABD",borderwidth=4,relief="solid")
            Label(taskwise_panel,text="Task {}".format(data[pk]["data"].index(task)+1),bg="#07EABD",font=task_number_font,fg="black").grid(row=0,column=0)
            task_name = Label(taskwise_panel,text=task["task_name"],bg="#07EABD",fg="black",font=("Heletivca",25,"bold underline"))
            task_name.grid(row=1,column=0)
            
            length = len(task["task"])
            original = task["task"]
            final = ""
            if length>50:
                task["task"] = (task["task"][:51]+"...")
            if length>25:
                while length>25:
                    if length>50:
                        final += task["task"][:25]+"\n"
                        task["task"] = task["task"][25:]
                        length-=25
                    else:
                        final += task["task"][:25]
                        task["task"] = task["task"][25:]
                        length-=25
            else:
                final=task["task"]
            final = final.rstrip()
            task["task"] = original
                
            task_info = Label(taskwise_panel,text=final,bg="#07EABD",fg="black",font=task_info_font)
            task_info.grid(row=2,column=0)
            task_date = Label(taskwise_panel,text=date_conversion(task["date"]),bg="#07EABD",fg="black",font=task_font)
            task_date.grid(row=3,column=0)
            task_time = Label(taskwise_panel,text=task["time"],bg="#07EABD",fg="black",font=task_font)
            task_time.grid(row=4,column=0)
            
            def confirm_task(pk,val):
                data = retrieve_data()
                for t in data[pk]["data"]:
                    if int(t["id"])==int(val):
                        cur = data[pk]["data"][data[pk]["data"].index(t)]
                        break

                rem = data[pk]["data"][:data[pk]["data"].index(t)]
                if cur["status"]=="Yes":
                    messagebox.showinfo("Task Incomplete.","Page will be updated upon app restart.")
                    cur["status"]="No"
                else:
                    messagebox.showinfo("Task Complete!","Page will be updated upon app restart.")
                    cur["status"]="Yes"

                rem.append(cur)
                rem.extend(data[pk]["data"][data[pk]["data"].index(t)+1:])
                data[pk]["data"]=rem
                
                with open("data.txt","w") as f:
                    for user in data:
                        f.write(str(user)+"\n")
                        f.write(r"%%//%%"+"\n")
                                    
            done = Checkbutton(taskwise_panel,text="Completed?",variable=task["id"],command=lambda pk=pk, val=task["id"]: confirm_task(pk,val),bg="#07EABD")
            if task["status"]=="Yes":
                done.select()
            else:
                done.deselect()

            done.grid(row=5,column=0)
            taskwise_panel.grid(row=cur,column=0,pady=10)
            cur+=1

        def page_based_task(page_number):
            change = data[pk]["data"][2*page_number-2:2*page_number]
            task_panel.grid_forget()
            wnd.update()
            tasks_display(change)

        #page nav
        for i in range(1,ceil(len(data[pk]["data"])/2)+1):
            but = Button(task_panel,text=i,bg="red",fg="white",font=('Helevitica',10,"bold"),command= lambda e=i: page_based_task(e))
            but.grid(row=cur,column=i)

        task_panel.grid(row=1,column=1,rowspan=10)
    tasks_display(data[pk]["data"][:2])

    buttons_frame = Frame(wnd,bg="#07EABD")
    
    def help_func():
        wnd = Tk()
        wnd.config(bg="#07EABD")
        wnd.geometry("400x500+200+200")
        wnd.iconbitmap('logo.ico')
        wnd.title("Help")
        
        def passme():
            pass
        add_tsk =  PhotoImage(master=wnd,file="planner.png")
        add_tsk_btn = Button(wnd,bg="#07EABD",relief="groove",command=passme)
        add_tsk_btn.config(image=add_tsk)
        add_tsk_btn.grid(row=0,column=0,padx=30,pady=15)
        add_tsk_label = Label(wnd,text="Allows user to add a task.",bg="#07EABD",fg="black",font=('Helevitica',13,"bold"))
        add_tsk_label.grid(row=0,column=1)

        change_date_img = PhotoImage(master=wnd,file='calendar.png')
        change_date = Button(wnd,command=passme,relief="groove")
        change_date.config(image=change_date_img)
        change_date.grid(row=1,column=0,pady=15)
        change_date_label = Label(wnd,text="Allows user to search for tasks\non a particular date.",bg="#07EABD",fg="black",font=('Helevitica',13,"bold"))
        change_date_label.grid(row=1,column=1)

        graph_ = Image.open("productivity.png")
        graph = ImageTk.PhotoImage(master=wnd,image=graph_)
        graph_button=Button(wnd,command=passme,relief="groove")
        graph_button.config(image=graph)
        graph_button.grid(row=2,column=0,pady=15)
        graph_button_label = Label(wnd,text="Allows user to find analytics\nregarding their productivtiy over\na certain time frame.",bg="#07EABD",fg="black",font=('Helevitica',13,"bold"))
        graph_button_label.grid(row=2,column=1)

        close_img = PhotoImage(master=wnd,file="close.png")
        close = Button(wnd,command=passme,relief="groove")
        close.config(image=close_img)
        close.grid(row=3,column=0,pady=15)
        close_label = Label(wnd,text="Allows user to logout.",bg="#07EABD",fg="black",font=('Helevitica',13,"bold"))
        close_label.grid(row=3,column=1)

        history_img = PhotoImage(master=wnd,file='history.png')
        history = Button(wnd,command=passme,relief="groove")
        history.config(image=history_img)
        history.grid(row=4,column=0,pady=15)
        history_label = Label(wnd,text="Allows user to check history of tasks added.",bg="#07EABD",fg="black",font=('Helevitica',13,"bold"))
        history_label.grid(row=4,column=1)

        wnd.mainloop()

    Label(buttons_frame,text="\n",bg="#07EABD").grid(row=0,column=0)
    help_img = PhotoImage(master=wnd,file="help.png")
    help_btn = Button(buttons_frame,command=help_func,relief="groove")
    help_btn.config(image=help_img)
    help_btn.grid(row=1,column=0)
    Label(buttons_frame,text="\n",bg="#07EABD").grid(row=2,column=0)
    add_tsk_img = PhotoImage(master=wnd,file="planner.png")
    add_tsk = Button(buttons_frame,command=lambda pk=pk: add_task(pk),relief="groove")
    add_tsk.config(image=add_tsk_img)
    add_tsk.grid(row=3,column=0)
    Label(buttons_frame,text="\n",bg="#07EABD").grid(row=4,column=0)
    change_date_img = PhotoImage(master=wnd,file='calendar.png')
    change_date = Button(buttons_frame,command=lambda var=pk: date_selection(var),relief="groove")
    change_date.config(image=change_date_img)
    change_date.grid(row=5,column=0)
    Label(buttons_frame,text="\n",bg="#07EABD").grid(row=6,column=2)
    '''graph= PhotoImage(master=wnd,file="productivity.png")
    '''
    graph_ = Image.open("productivity.png")
    graph = ImageTk.PhotoImage(graph_)
    graph_button=Button(wnd,command=lambda var=pk: graph_display(var),relief="groove")
    graph_button.config(image=graph)
    graph_button.grid(row=7,column=2)
    Label(buttons_frame,text="\n",bg="#07EABD").grid(row=8,column=2)
    history_img = PhotoImage(master=wnd,file="history.png")
    history = Button(wnd,command=lambda: normalstack(),relief="groove")
    history.config(image=history_img)
    history.grid(row=10,column=2)


    buttons_frame.grid(row=1,column=2,rowspan=10)
    wnd.mainloop()

def login(cur):
    if cur!="No Window Yet.":
        confirm = messagebox.askyesno("Confirmation","Are you sure you want to logout?")
        if confirm==True:
            cur.destroy()
            time.sleep(0.5)
        else:
            return None
        
    wnd = Tk()
    wnd.geometry("300x350+150+150")
    wnd.config(bg="#07EABD")
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="LOGIN",font=("Heletivca",28,"bold"),bg="#07EABD",fg="black").pack()
    Label(wnd,text="----------------------------------------------------------",font=("Heletivca",4,"bold"),bg="#07EABD",fg="black").pack()
    Label(wnd,text="",bg="#07EABD").pack()
    Label(wnd,text="USERNAME",font=("Heletivca",24,"bold"),bg="#07EABD",fg="black").pack()
    username = ttk.Entry(wnd,font=("Heletivca",16,"bold"))
    username.pack()
    Label(wnd,text="",bg="#07EABD").pack()
    Label(wnd,text="PASSWORD",font=("Heletivca",24,"bold"),bg="#07EABD",fg="black").pack()
    password = ttk.Entry(wnd,font=("Heletivca",16,"bold"),show="*")
    password.pack()
    Label(wnd,text="",bg="#07EABD").pack()

    def authenticate(event):
        usern = username.get()
        pswd = Encryption(password.get())
        pswd = pswd.encrypt(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
        data = retrieve_data()

        c=0
        if len(usern)==0 or len(pswd)==0:
            messagebox.showerror("LoginError","Kindly fill in the Credentials.")
            login(wnd)
        for user in data:
            if user["username"]==usern and user["pass"]==pswd:
                messagebox.showinfo("Authenticated!","Successfully logged in!")
                wnd.destroy()
                c+=1
                homepage(data.index(user))
        if c==0:
            messagebox.showerror("LoginError","Username Entered Does Not Exist.")
            login(wnd)
                    
    submit = Button(wnd,text="SUBMIT",font=("Heletivca",20,"bold"),bg="#386B09",fg="yellow")
    submit.bind('<Button-1>',authenticate)
    submit.pack()
    wnd.mainloop()
    
login("No Window Yet.")
