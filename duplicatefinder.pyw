from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from datetime import datetime
import sys
import hashlib
import os

BUF_SIZE = 65536

rootdir = ""
file_count = 0

root = Tk()

button = ttk.Button(root, text="Set Directory")
button_calc_sha = ttk.Button(root, text="Calculate Hash")

lbl_directory = ttk.Label(root, text="")

def open_file_dialog():
    global rootdir
    rootdir =  filedialog.askdirectory()
    lbl_directory.configure(text=rootdir)

def calc_sums(path, file):
    sums_list = []

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(os.path.join(path, file), 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha256.update(data)

    sums_list.append(md5.hexdigest())
    sums_list.append(sha1.hexdigest())
    sums_list.append(sha256.hexdigest())
    
    return sums_list
    
def get_date():
    date = str(datetime.now())
    date_chars = [" ", ":", "-"]

    for chars in date_chars:
        date = date.replace(chars, "")
        
    date = date.split('.', 1)[0]
    return date

def log_sums():
    global rootdir
    
    sha256_file = open(get_date() + "_file_sums.txt", "w+")    

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            sums_list = calc_sums(subdir, file)

            sha256_file.write("File name: " + file + "\n")
            sha256_file.write("MD5:\t{0}\n".format(sums_list[0]))
            sha256_file.write("SHA1:\t{0}\n".format(sums_list[1]))
            sha256_file.write("SHA256:\t{0}\n\n".format(sums_list[2]))
            
    sha256_file.close()

button.config(command = open_file_dialog)
button_calc_sha.config(command = log_sums)

button.grid(row=2, column=1)
button_calc_sha.grid(row=3, column=1)

lbl_directory.grid(row=2, column=2)

root.mainloop()
