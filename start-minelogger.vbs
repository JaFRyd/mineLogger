Set WshShell = CreateObject("WScript.Shell")

' Kill any process currently listening on port 5001
WshShell.Run "powershell -WindowStyle Hidden -Command """ & _
    "$pids = (Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue).OwningProcess | Sort-Object -Unique;" & _
    "foreach ($p in $pids) { Stop-Process -Id $p -Force -ErrorAction SilentlyContinue }" & _
    """", 0, True

' Give the port a moment to be released
WScript.Sleep 1200

' Start the server (hidden window)
WshShell.Run """C:\Users\tyl\Sync\PrivateCoding\mineLogger\.venv\Scripts\python.exe"" ""C:\Users\tyl\Sync\PrivateCoding\mineLogger\main.py"" ui --port 5001", 0, False

' Wait for Flask to be ready, then open the browser
WScript.Sleep 2000
WshShell.Run "explorer ""http://localhost:5001""", 0, False
