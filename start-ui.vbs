Set WshShell = CreateObject("WScript.Shell")
Dim basePath, port
basePath = Replace(WScript.ScriptFullName, "start-ui.vbs", "")

' Read port from port.txt, fall back to 5001
port = "5001"
On Error Resume Next
Dim fso, f
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.OpenTextFile(basePath & "port.txt", 1)
port = Trim(f.ReadLine())
f.Close
On Error GoTo 0

' Start server hidden (window style 0 = no window)
WshShell.Run """" & basePath & "minelogger.exe"" ui --no-browser --port " & port, 0, False

' Wait for server to start, then open browser
WScript.Sleep 2000
WshShell.Run "explorer ""http://localhost:" & port & """", 0, False
