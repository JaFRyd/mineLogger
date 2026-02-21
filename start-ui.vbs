Set WshShell = CreateObject("WScript.Shell")
Dim basePath
basePath = Replace(WScript.ScriptFullName, "start-ui.vbs", "")

' Start server hidden (window style 0 = no window)
WshShell.Run """" & basePath & "minelogger.exe"" ui --no-browser", 0, False

' Wait for server to start, then open browser
WScript.Sleep 2000
WshShell.Run "explorer ""http://localhost:5000""", 0, False
