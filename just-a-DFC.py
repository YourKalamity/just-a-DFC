#!/usr/bin/env python3

import ctypes
import os
import platform
import sys

def getFreeSpace(dirname):
    #Returns Space remaining in GB
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
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
    print("Creating dummy files...")
    print("Please wait...")
    with open(dummyFileLocation, 'ab') as dummyFile:
        numChars = amount * 1024 * 1024 * 1024  + 10240000
        x = 0
        toWrite = '1'.encode()
        while x < numChars:
            dummyFile.write(toWrite)
            x = x + 1

    print("A dummy file has been created and saved as dummy1 on the root of the SD card")
    print("You may move this file to a different folder")
    print("")
    print("To double check you could run this program after it has closed")
    print("to calculate if the free space is now ok")
    print("This application will now close")
    input()
    sys.exit()

def main():
    if(sys.version_info.major < 3):
        print("This program will ONLY work on Python 3 and above")
        sys.exit()
    
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

