import win32com.client

strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("Select * from Win32_Process")
for objItem in colItems:
   if (objItem.Name == "telservice.exe"):
      print("Found telservice!")
   elif (objItem.Name == "ngrok.exe"):
      print("Found ngrok!")
   else:
      pass
