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
        if driveLetter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print("That's not a valid input")
        try:
            directory = driveLetter + ":/dummy1"
            with open(directory, 'ab') as file:
                file.close()
        except FileNotFoundError:
            print("You do not have write access or the drive could not be found")
        except PermissionError:
            print("You do not have write access")
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
        numChars = amount * 1024 * 1024 * 1024  + 10
        x = 0
        thing = '1'.encode()
        while x < numChars:
            dummyFile.write(thing)
            x = x + 1

    print("A dummy file has been created and saved as dummy1 on the root of the SD card")
    print("This application will now close")
    sys.exit()

def main():
    if platform.system() == 'Windows':
        driveLetter = getDriveLetter()
        print(driveLetter)
        freeSpace = getFreeSpace(driveLetter + ":/")
    else:
        print("Please use Windows to run this program")
        sys.exit()
        
    print("Free space remaining (in GB) = ", freeSpace)

    sizeOfDummyFiles = dummyFilesNeeded(freeSpace)

    dummyFileLocation = driveLetter + ":/dummy1"

    createDummyFiles(sizeOfDummyFiles,dummyFileLocation)

main()

