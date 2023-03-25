import os
import pyfiglet
import win32api



class StorageSpider():

    def __init__(self):
        self.absPath = r''

    def appBanner(self):
        logo = pyfiglet.figlet_format("S t o r a g e", font='epic')
        logo1 = pyfiglet.figlet_format(" S p i d e r", font='epic')
        red = "\033[1;31m"
        green = "\033[1;32m"
        print(green + logo + red + logo1)

    def listDisks(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        return drives

    def convert_bytes(self, size):
        """ Convert bytes to KB, or MB or GB"""
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    def getMbFileSize(self, file):
        filestat = os.path.getsize(file)
        return self.convert_bytes(filestat)

    def getDirSize(self, dir):
        nbytes = sum(d.stat().st_size for d in os.scandir(dir) if d.is_file())
        return self.convert_bytes(nbytes)

    def searchAll(self, disk):
        ss = ""
        for relPath, dirs, files in os.walk(disk):
            for i in dirs:
                file = os.path.join(relPath, i)
                ss += file+"\n"
        return ss

    def layerSearch(self, disk):
        os.system("cls")
        print("\n"*1000)
        self.appBanner()
        ss = ""
        idx = 0
        for dir in range(0, len(os.listdir(disk))):
            if idx % 2 == 0:
                ss += '{:<50s}'.format("("+str(idx)+") "+os.listdir(disk)[idx]) + "\t"
            else:
                ss += '{:<50s}'.format("(" + str(idx) + ") " + os.listdir(disk)[idx]) + "\n"
            idx += 1
        return "\n"+ss

    def describe(self, data, start_idx=0, end_idx=50):
        return data[start_idx:end_idx]

    def goBack(self, absPath):
        self.absPathx = absPath.split("\\")
        self.absPath = ""
        for x in self.absPathx:
            if x == '':
                self.absPathx.pop(self.absPathx.index(x))
        self.absPathx.pop(self.absPathx.index(self.absPathx[-1]))
        for pt in self.absPathx:
            self.absPath += pt + "\\"
        return self.absPath

    def rename(self):
        newName = input("New name: ")
        os.rename(self.absPath, self.goBack(self.absPath)+newName)
        print(self.layerSearch(self.goBack(self.absPath+newName)))

    def move(self):
        try:
            newPath = input("New path: ")
            os.rename(self.absPath, newPath)
            print("moved to new path!\n")
            print(self.layerSearch(self.goBack(newPath)))
        except OSError:
            print("\nCan't do this process!\n")

    def newDir(self):
        try:
            newFolder = input("Folder name: ")
            print(self.absPath + "\\" + newFolder)
            os.mkdir(self.absPath + "\\" + newFolder)
            print("Folder created!")
            print(self.layerSearch(self.absPath))
        except OSError:
            print("\nCan't do this process!\n")

    def newFile(self):
        try:
            newFile = input("File name: ")
            print(self.absPath + "\\" + newFile)
            with open(self.absPath + "\\" + newFile, 'w') as f:
                f.write("")
            f.close()
            print("File created!")
            print(self.layerSearch(self.absPath))
        except OSError:
            print("\nCan't do this process!\n")

    def delete(self):
        if os.path.isdir(self.absPath):
            try:
                sw = input("Type (Yes) if you sure!")
                if sw == "Yes":
                    os.rmdir(self.absPath)
                    print("\nFolder deleted.\n")
                else:
                    print("\nCanceled.\n")
            except OSError:
                print("\nCan't delete this folder!\n!! maybe some files inside folder prevent delete operation!")
        else:
            sw = input("Type (Yes) if you sure!")
            if sw == "Yes":
                os.remove(self.absPath)
                print("\nFile deleted.\n")
                self.absPath = self.goBack(self.absPath)
            else:
                print("\nCanceled.\n")


if __name__ == "__main__":
    ss = StorageSpider()
    ss.appBanner()
    while 1:
        disks = ss.listDisks()
        for disk in range(0, len(disks)):
            print("(" + str(disk) + ") " + disks[disk])
        print("(B) Back\n")
        diskChoose = input("select: ")
        if diskChoose.isdecimal():
            ss.absPath += ss.listDisks()[int(diskChoose)]
            print(ss.layerSearch(ss.listDisks()[int(diskChoose)]))
            print("\n(ND)New Folder (NF)New File (D)Delete (R)Rename (M)Move (S)Size (G)Absolute path (L)List (B)Back\n")
        else:
            if diskChoose.lower() == "b":
                break
            else:
                print("\nUnknown option!\n")
        while 1:
            choose = input("select: ")
            if choose.isalpha():
                if choose.lower() == "nd" and os.path.isdir(ss.absPath):
                    ss.newDir()
                elif choose.lower() == "nf" and os.path.isdir(ss.absPath):
                    ss.newFile()
                elif choose.lower() == "d":
                    ss.delete()
                elif choose.lower() == "r":
                    ss.rename()
                elif choose.lower() == "s":
                    if os.path.isfile(ss.absPath):
                        print("File size: ", ss.getMbFileSize(ss.absPath))
                    else:
                        print("in Folder files size: ", ss.getDirSize(ss.absPath))
                elif choose.lower() == "g":
                    print("\n"+ss.absPath+"\n")
                elif choose.lower() == "m":
                    ss.move()
                elif choose.lower() == "b":
                    if len(ss.absPath) < 4:
                        ss.absPath = r""
                        break
                    else:
                        ss.absPath = ss.goBack(ss.absPath)
                        print(ss.layerSearch(ss.absPath))
                        print("\n(ND)New Folder (NF)New File (D)Delete (R)Rename (M)Move (S)Size (G)Absolute path (L)List (B)Back\n")
                elif choose.lower() == "l" and os.path.isdir(ss.absPath):
                    print(ss.layerSearch(ss.absPath))
                else:
                    print("\nUnknown choice!\n")
            elif choose.isdecimal() and os.path.isdir(ss.absPath):
                try:
                    ss.absPath += "\\" + os.listdir(ss.absPath)[int(choose)]
                    if os.path.isdir(ss.absPath):
                        print(ss.layerSearch(ss.absPath))
                        print("\n(ND)New Folder (NF)New File (D)Delete (R)Rename (M)Move (S)Size (G)Absolute path (L)List (B)Back\n")
                    else:
                        print(ss.absPath)
                        print("\n(D)Delete (R)Rename (M)Move (S)Size (G)Absolute path (B)Back\n")
                except IndexError:
                    print("\nUnlisted option!!\n")
                    print(ss.layerSearch(ss.absPath))
                    print("\n(ND)New Folder (NF)New File (D)Delete (R)Rename (M)Move (S)Size (G)Absolute path (L)List (B)Back\n")
            else:
                print("\nUnknown choice!\n")
