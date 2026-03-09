Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Users\tyl\Sync\PrivateCoding\mineLogger\.venv\Scripts\python.exe"" ""C:\Users\tyl\Sync\PrivateCoding\mineLogger\main.py"" ui --port 5001", 0, False
WScript.Sleep 2000
WshShell.Run "explorer ""http://localhost:5001""", 0, False
