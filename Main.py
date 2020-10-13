import os
import time
import shutil
import subprocess
import pathlib


def clrscr():
    os.system('cls')


def driveList():
    c = 1
    l = []
    for drive_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if os.path.exists(f'{drive_letter}:/'):
            print(f'{c}. {drive_letter}:/')
            c+=1
            l.append(F'{drive_letter}:/')
        else:
            pass
    inp = input()
    if l[int(inp) - 1] in l:
        currentPath = l[int(inp) - 1]
        return currentPath
    else:
        clrscr()
        print("Choose a drive:")
        return driveList()


cwd = ""
cwd2 = ""
cpy = ""

# Shows list of directories/files and returns selected file
def display_files(currentPath): # takes path and returns selected dir/file path
    clrscr()
    dirList = os.listdir(currentPath)
    print(f'Directory: {currentPath}')
    print("-"*150)
    global cwd
    cwd = currentPath
    print("0. Main Menu")
    print("1. .")
    c = 2
    l = []
    for i in dirList:
        print(f"{c}. {i}")
        c += 1
        l.append(i)
    print("-"*150)
    if cwd2 == "":
        print(f'Options:    (a). Create a Folder  (b). Delete a Folder   (c). Create a File')
    elif cpy == "True":
        print("Press 'D' to copy here")
    else:
        print("Press 'M' to move here")
    o = input()
    if o == str(0):
        cwd = ""
        fileManager()
    elif o == str(1):
        currentPath = f'{pathlib.Path(currentPath).parent}/'
        return display_files(currentPath)
    elif o.lower() == "exit":
        exit()
    elif o.lower() in ('a', 'b', 'c'):
        return o.lower()
    elif o.lower() == 'd':
        return 'd'
    elif o.lower() == 'm':
        return 'm'
    elif int(o) <= c-1:
        path = f'{currentPath}{l[int(o) - 2]}/'
        if os.path.isdir(path):
            return display_files(path)
        else:
            return l[int(o) - 2], currentPath
    else:
        display_files(cwd)

# File Options functions
def readFile(fname):
    clrscr()
    print(f"File: {fname}")
    print("-"*150)
    f = open(fname, "r")
    print(f.read())
    print("-"*150)
    print("Options: 1. Back to folder")
    o = input()
    if o == str(1):
        fileManager()
    else:
        print("Invalid Selection")
        time.sleep(3)
        readFile(fname)

def writeFile(fname):
    clrscr()
    print(f"File: {fname}")
    print("-"*150) 
    p = open(fname, "r")
    print(p.read())
    print("---------CAUTION: The file will be overwritten-----------")
    f = open(fname, "w")
    n = input()
    f.write(n)
    f.close()
    fileManager()


def appendText(fname):
    f = open(fname, "a")
    n = input()
    f.write(n)
    f.close()
    fileManager()

def deleteFile(fname):
    fpath = os.path.join(cwd, fname)
    os.remove(fpath)
    fileManager()

def file_options(fname, path):
    clrscr()
    print(f'Directory: {path}')
    print(f'File: {fname}')
    print(f'Options:'+ '\n' + '1. Read' + '\n' + '2. Edit' + '\n' + '3. Append' +'\n' + '4. Delete' + '\n' + \
          '5. Copy' +'\n' +'6. Move' + '\n' + '7. Back to folder')
    o = input()
    if o.lower() == "exit":
        exit()
    elif o in ['1','2','3','4','7']:
        return int(o)
    elif o == '5':
        global cpy
        cpy = "True"
        return int(o)
    elif o == '6':
        global cwd2
        cwd2 = cwd
        return int(o)
    else:
        file_options(fname, path)

def copyFile(fname):
    global cwd2, cpy
    cwd2 = cwd
    k = display_files(cwd)
    path1 = os.path.join(cwd2, fname)
    path2 = os.path.join(cwd, fname)
    if k == 'd':
        shutil.copy2(path1, path2)
    else:
        pass
    cwd2 = ""
    cpy = ""
    fileManager()

def moveFile(fname):
    global cwd2
    k = display_files(cwd)
    path1 = os.path.join(cwd2, fname)
    path2 = os.path.join(cwd, fname)
    if k == 'm':
        shutil.move(path1, path2)
    else:
        pass
    cwd2 = ""
    fileManager()


# Folder level options functions
def createDirectory():
    clrscr()
    print(f'Directory: {cwd}')
    o = input("Create Folder: ")
    path = os.path.join(cwd, o)
    try:
        os.mkdir(path, 0o755)
    except OSError:
        print("Creation of folder failed")
    else:
        print("Successfully created the directory.")
        time.sleep(2)
    fileManager()


def deleteDirectory():
    clrscr()
    print(f'Directory: {cwd}')
    o = input("Delete Folder: ")
    path = os.path.join(cwd, o)
    try:
        os.rmdir(path)
    except OSError:
        print("Deletion of the directory failed")
    else:
        print("Successfully deleted the directory.")
        time.sleep(2)
    fileManager()

def createFile():
    clrscr()
    print(f'Directory: {cwd}')
    o = input("Create File: ")
    try:
        open(o,"w+")
    except OSError:
        print("Creation of file failed")
    else:
        print("Successfully created the file.")
        time.sleep(2)
    fileManager()


# Main Menu
def mainMenu():
    global cwd
    if cwd == "":
        clrscr()
        print("                         ####### Python File Manager ######## ")
        print("Read a file")
        print("Write to a file")
        print("Append text to a file")
        print("Delete a file")
        print("Move a file")
        print("Copy a file")
        print("Create a directory")
        print("Delete a directory")
        print("Open a program")
        print("-"*150)
        print("Use numbers to browse.")
        print("Type 'Exit' to exit the program.")
        print("Press enter to continue.")
        o = input()
        if o == "":
            clrscr()
            print("Choose a drive:")
            return driveList()
        elif o.lower() == "exit":
            exit()
        else:
            mainMenu()
    else:
        return cwd


def fileManager():
    o = mainMenu()
    k = display_files(o)
    if isinstance(k, tuple):
        m = file_options(k[0], k[1])
        if m == 1:
            readFile(k[0])
        elif m == 2:
            writeFile(k[0])
        elif m == 3:
            appendText(k[0])
        elif m == 4:
            deleteFile(k[0])
        elif m == 5:
            copyFile(k[0])
        elif m == 6:
            moveFile(k[0])
        elif m == 7:
            return fileManager()
    else:
        if k == 'a':
            createDirectory()
        if k == 'b':
            deleteDirectory()
        if k == 'c':
            createFile()


fileManager()










