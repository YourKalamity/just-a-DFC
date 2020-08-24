#!/usr/bin/env python3
#
# Created by YourKalamity

import ctypes
import os
import platform
import sys
import tkinter
import tkinter.font 
from tkinter import filedialog
from tkinter import messagebox
import threading
import tkinter.ttk

def chooseDir(source,entryBox):
    source.sourceFolder =  filedialog.askdirectory(parent=source, initialdir= "/", title='Please select the directory of your SD card')
    entryBox.delete(0, tkinter.END)
    entryBox.insert(0, source.sourceFolder)

def outputbox(message):
    outputBox.configure(state='normal')
    outputBox.insert('end', message+"\n")
    outputBox.see(tkinter.END)
    outputBox.configure(state='disabled')

def threadFunction(location, source):
    startThread = threading.Thread(target=start, daemon=True, args=(location,source,))
    startThread.start()

def getFreeSpace(dirname):
    #Returns Space remaining in GB
    print(dirname)
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        print(free_bytes.value / 1024 / 1024 / 1024)
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024 /1024

def donothing():
    return

def closeButtonPress(source):
    source.destroy()


def createDummyFiles(amount,dummyFileLocation):
    outputbox("Creating...")
    outputbox("Please wait...")
    with open(dummyFileLocation, 'ab') as dummyFile:
        x = 0
        toWrite = '1'.encode()
        while x < numChars:
            dummyFile.write(toWrite)
            x = x + 1

    outputbox("DF Created")
    outputbox("Close App")
    return

def start(location,source):
    window.protocol("WM_DELETE_WINDOW",lambda:donothing)
    startButton.config(state="disabled")
    outputBox.configure(state='normal')
    outputBox.delete('1.0', tkinter.END)
    outputBox.configure(state='disabled')
    print(location)
    try:
        if location.endswith("/"):
            location = location[:-1]
        directory = location + "/dummy1.dfc"
        print(directory)
        with open(directory, 'ab') as file:
            file.close()
    except FileNotFoundError:
        outputbox("Access Error")
        startButton.config(state="normal")
        window.protocol("WM_DELETE_WINDOW",lambda:closeButtonPress(window))
        return
    except PermissionError:
        outputbox("Access Error")
        startButton.config(state="normal")
        window.protocol("WM_DELETE_WINDOW",lambda:closeButtonPress(window))
        return

    freeSpace = getFreeSpace(location)
    outputbox("Free Space: ")
    outputbox(str(freeSpace) + "GB")
    if (freeSpace % 4) <= 2:
        outputbox("Dummy not needed")
        startButton.config(state="normal")
        window.protocol("WM_DELETE_WINDOW",lambda:closeButtonPress(window))
        return
    else:
        requiredAmount = (freeSpace % 4) - 2
        outputbox(str(requiredAmount) + "GB needed")
        createDummyFiles(requiredAmount, directory)
        startButton.config(state="normal")
        window.protocol("WM_DELETE_WINDOW",lambda:closeButtonPress(window))
        return


def main():
    if(sys.version_info.major < 3):
        print("This program will ONLY work on Python 3 and above")
        sys.exit()
    global window
    window = tkinter.Tk()
    window.minsize(100,100)
    window.resizable(0,0)
    titleFont = tkinter.font.Font(size=20)
    title = tkinter.Label(window, text="just-a-DFC", font=titleFont)
    title.grid(row=0,column=0,sticky="w")
    SDEntry = tkinter.Entry(width=20)
    SDEntry.grid(column=0, row=2)
    chooseDirButton = tkinter.Button(window, text = "Click to select SD", command =lambda:chooseDir(window,SDEntry),width=20)
    chooseDirButton.grid(column=0, row=3,pady=1)
    global outputBox
    outputBox = tkinter.Text(window,state='disabled', width = 20, height = 5, bg="black", fg="white")
    outputBox.grid(column=0,row=4,sticky="w")
    global startButton
    startButton = tkinter.Button(window,text="Start", command =lambda:threadFunction(SDEntry.get(),window,), width=10, font=("Segoe UI", 11))
    startButton.grid(column=0,row=6)
    
    


    window.mainloop()

main()

