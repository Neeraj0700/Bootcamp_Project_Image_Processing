#Importing necessary libraries
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from PIL import Image
import pytesseract
import pandas as pd
import cv2
import  mysql.connector

#establishing connection to MySQL database
conn = mysql.connector.connect(user='root', password='sharma072418', host='127.0.0.1', database='Feedback', auth_plugin='mysql_native_password')

#Creating new root window and defining its size and other properties
root = tk.Tk()
root.config(bg="peach puff")
Title = root.title("OCR GUI")
root.geometry('661x300')
root.resizable(0, 0)

#Function to add entries of feedback section to database
def register():
    name1 = name.get()
    email1 = email.get()
    feedback1 = feedback.get()
    if name1 == '' or email1 == '' or feedback1 == '':
        messagebox.showerror(title='Error', message='Fill the empty fields!')
    else:
        cursor = conn.cursor()
        insert_stmt = (
            "INSERT INTO feed(NAME, EMAIL, MESSAGE)"
            "VALUES (%s, %s, %s)"
        )
        data = (name1, email1,feedback1)
        try:
            # executing the sql command
            cursor.execute(insert_stmt, data)
            # commit changes in database
            conn.commit()
        except:
            conn.rollback()
        tkmsg = messagebox.showinfo(title='Successful', message='Thank you for your valuable feedback')

#If user chooses 1st Option then this function will execute
def readfromimage1():
    path = PathTextBox.get('1.0', 'end-1c')
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    im = cv2.imread(path)                                                                           #reading image from given path
    #Image Preprocessing
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)                                                       #Converting Image to Grayscale
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)  #Implementing Adaptive thresholding on grayscale Image
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    im = cv2.filter2D(im, -1, kernel)                                                               #Sharpen the pixels of image Using Kernel
    text = pytesseract.image_to_string(im, lang='eng')
    excel_file = r'C:\Users\visha\Desktop\Text Extraction\Knowledge Base.xlsx'                  #Reading the knowledge Base
    df = pd.read_excel(excel_file)
    with open(r'file1.txt', mode='w') as f:
        f.write(text.upper())
    frames = []
    with open('file1.txt', 'r') as file:
        for line in file:
            for word in line.split():
                df1 = df[df['WORDS'] == word]
                frames.append(df1)
    if frames:
        result = pd.concat(frames)
    else:
        print("No results")


    export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')       #On successfull completion A window opens to ask user where
                                                                                    #to save output excel file
    result.to_excel(export_file_path, index=False, header=True)


#If user chooses second option this function will execute
def readfromimage2():
    path = PathTextBox.get('1.0', 'end-1c')
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    im = cv2.filter2D(im, -1, kernel)
    text = pytesseract.image_to_string(im, lang='eng')
    excel_file = r'C:\Users\visha\Desktop\Text Extraction 2\Knowledge_Base 2.xlsx'
    df = pd.read_excel(excel_file)
    with open(r'file1.txt', mode='w') as f:
        f.write(text.upper())
    frames = []
    with open('file1.txt', 'r') as file:
        for line in file:
            for word in line.split():
                df1 = df[df['WORDS'] == word]
                frames.append(df1)
    if frames:
        result = pd.concat(frames)
    else:
        print("No matching Values")

    export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    result.to_excel(export_file_path, index=False, header=True)

#Deopdown menu function to decide which function will execute when
def checkcmbo():

    if Operation.get() == "Get Synonyms and Antonyms":
        readfromimage1()

    elif Operation.get() == "Get Meaning in different Languages":
        readfromimage2()


#Fuction to browse image from user's System
def openfile():
    name = askopenfilename(initialdir="/",
                           filetypes=(("PNG File", "*.png"), ("BMP File", "*.bmp"), ("JPEG File", "*.jpeg")),
                           title="Choose a file."
                           )
    PathTextBox.delete("1.0", END)
    PathTextBox.insert(END, name)

#Confirm to exit Function
def confirmation():
    MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        root.destroy()
    else:
        tk.messagebox.showinfo('Return', 'You will now return to the application screen')

#Creating Feedback window
def createfeedbackWindow():
    newWindow = tk.Toplevel(root)
    newWindow.geometry('500x355')
    newWindow.config(bg="peach puff")
    newWindow.title('Send Feedback')
    newWindow.resizable(0,0)
    global name
    global email
    global feedback
    global message2
    name = StringVar()
    email = StringVar()
    feedback = StringVar()
    message2 = StringVar()
    label3 = Label(newWindow, text=' Feedback Form ',background = 'salmon', foreground ="white", font = ("Times New Roman", 15),anchor=N)
    label3.place(x=250, y=20, anchor=CENTER)
    label4 = Label(newWindow, text=" Name :", font=("Times New Roman", 10))
    label4.grid(column=0, row=2, padx=10, pady=60, sticky=W)
    t1 = tk.Entry(newWindow, textvariable=name, width=31)
    t1.grid(row=2, column=2, padx=24)
    label6 = Label(newWindow, text="Email :", font=("Times New Roman", 10))
    label6.place(x=10,y=100)
    t3 = tk.Entry(newWindow,  textvariable=email)
    t3.place(x=90,y=100,width=190)
    label7 = Label(newWindow, text="Feedback :", font=("Times New Roman", 10))
    label7.place(x=10, y=150)
    t4 = tk.Entry(newWindow,  textvariable=feedback, width='50')
    t4.place(x=90, y=150, width=370, height=100)
    ReadButton1 = Button(newWindow, text=" Submit ", command=register, bg='salmon', fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
    ReadButton1.place(x=215, y=270)
    exit = Button(newWindow, text=" Exit ", command=lambda: newWindow.destroy(), bg='salmon', fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
    exit.place(x=226, y=315)




label1 = Label(root, text = " Text Extraction From Image Using Tesseract OCR ",  background = 'salmon', foreground ="white", font = ("Times New Roman", 15),anchor=N)
label1.place(x=330, y=20, anchor=CENTER)

label2 = Label(root, text = "Select Operation :", font = ("Times New Roman", 10))
label2.grid(column = 0, row = 2, padx = 10, pady = 60, sticky=W)

n = tk.StringVar()
Operation = ttk.Combobox(root, width = 30, textvariable = n)
Operation['values'] =('Get Synonyms and Antonyms',
                      'Get Meaning in different Languages')
Operation.place(x=135, y=59)

PathLabel = Label(root, text=" Browse Your File (Image): ",font = ("Times New Roman", 10))
PathLabel.place(x=10,y=116)

BrowseButton = Button(root, text=" Browse ", command=openfile, bg='salmon', fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
BrowseButton.place(x=573,y=110)

PathTextBox = Text(root, height=2, borderwidth=0, relief="sunken")
PathTextBox.grid(row=12, column=0, padx=10, pady=10)

ReadButton = Button(root, text=" Submit ", command=checkcmbo, bg='salmon', fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
ReadButton.place(x=286, y=200)

exitbutton = Button(root, text=" Exit ", command=confirmation, bg="salmon", fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
exitbutton.place(x=298, y=250)

feedbackbutton = Button(root, text=" Feedback ", command=createfeedbackWindow, bg="salmon", fg='white', font=("Times New Roman", 14), borderwidth=0, relief="sunken")
feedbackbutton.place(x=559, y=200)

Operation.current()
root.mainloop()

