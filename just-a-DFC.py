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
def getDriveName():
    while True:
        try:
            driveName = str(input("Enter the drive name of your SD card :   "))
        except TypeError:
            print("That's not a valid input")
            continue
        try:
            directory = '/Volumes/' + driveName + "/dummy1"
            with open(directory, 'ab') as file:
                file.close()
        except FileNotFoundError:
            print("You do not have write access or the drive could not be found")
            continue
        except PermissionError:
            print("You do not have write access")
            continue
        else:
            return driveName

def donothing():
    return

def closeButtonPress(source):
    source.destroy()

def getDriveDirectory():
    while True:
        try:
            print("Enter the FULL directory of your SD card")
            print("For example '/dev/sda1' without the quotation marks")
            driveDirectory = str(input("Full directory of your SD card : "))
            if driveDirectory[-1] == '/' :
                driveDirectory = driveDirectory[:--1]
            
        except TypeError:
            print("That's not a valid input")
            continue
        try:
            directory = driveDirectory + "/dummy1"
            with open(directory, 'ab') as file:
                file.close()
        except FileNotFoundError:
            print("You do not have write access or the drive could not be found")
            continue
        except PermissionError:
            print("You do not have write access")
            continue
        else:
            return driveDirectory

def getDriveLetter():
    while True:
        try:
            driveLetter = str(input("Enter the drive letter of your SD card :   "))
            driveLetter = driveLetter.upper()
        except TypeError:
            print("That's not a valid input")
            continue
        if len(driveLetter) != 1:
            print("That's not a valid input")
            continue
        if driveLetter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or driveLetter == '/' :
            print("That's not a valid input")
            continue
        try:
            directory = driveLetter + ":/dummy1"
            with open(directory, 'ab') as file:
                file.close()
        except FileNotFoundError:
            print("You do not have write access or the drive could not be found")
            continue
        except PermissionError:
            print("You do not have write access")
            continue
        else:
            return driveLetter
            break
def dummyFilesNeeded(freeSpace):
    x =  freeSpace % 4
    if x <= 2:
        print("Dummy files aren't necessary!")
        print("The application will now close")
        sys.exit()
    else:
        z = x - 2
        print(z,"GB of dummy files are needed")
        return z

def createDummyFiles(amount,dummyFileLocation):
    outputbox("Creating...")
    outputbox("Please wait...")
    with open(dummyFileLocation, 'ab') as dummyFile:
        numChars = amount * 1024 * 1024 * 1024  + 10240000
        x = 0
        toWrite = '1'.encode()
        while x < numChars:
            dummyFile.write(toWrite)
            x = x + 1

    outputbox("DF Created")
    outputbox("Close App")
    sys.exit()

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
    startButton.grid(column=0,row=5)


    window.mainloop()
    
    print("Just Kalam's just a dummy file creator (for hiyaCFW)")
    print(" ")
    print("This program will calculate if a dummy file is needed ")
    print("to insure hiyaCFW does not boot into the 'An error has")
    print("occured' screen")
    print("")
    if platform.system() == 'Windows':
        print('Platform : "Windows" ')
        driveLetter = getDriveLetter()
        directory = driveLetter + ":/"
        freeSpace = getFreeSpace(directory)
    elif platform.system() == 'Darwin':
        print('Platform : "MacOS X" ')
        driveName = getDriveName()
        directory = '/Volumes/' + driveName + "/"
        freeSpace = getFreeSpace(directory)
    elif platform.system() == 'Linux':
        print('Platform : "Linux"')
        driveDirectory = getDriveDirectory()
        freeSpace = getFreeSpace(driveDirectory)
    else:
        sys.exit()
        
    print("Free space remaining (in GB) = ", freeSpace)

    sizeOfDummyFiles = dummyFilesNeeded(freeSpace)

    dummyFileLocation = directory + "dummy1"

    createDummyFiles(sizeOfDummyFiles,dummyFileLocation)

main()

