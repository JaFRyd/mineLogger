Set WshShell = CreateObject("WScript.Shell")
Dim exePath
exePath = Replace(WScript.ScriptFullName, "start-silent.vbs", "minelogger.exe")
WshShell.Run """" & exePath & """ ui --no-browser", 0, False
