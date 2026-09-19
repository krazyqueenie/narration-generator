Option Explicit
Dim shell, fso, folder, command

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

folder = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = folder

command = "pythonw.exe " & Chr(34) & folder & "\narrate_web.py" & Chr(34)
shell.Run command, 1, False
