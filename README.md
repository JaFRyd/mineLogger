# mineLogger

A local work logger for tracking time spent on customer projects. Log entries from
the terminal or through a browser-based web UI. Data is stored in a local SQLite
database — nothing is sent to any external service.

---

## What it does

- Add time entries (date, customer, hours, description)
- List entries filtered by date range or customer
- Export entries to CSV
- Web UI with three tabs: Add Entry, View Log, Export

---

## Windows Installer (recommended for Windows users)

Download and run `minelogger-setup.exe`. The installer:

- Installs mineLogger to `C:\Program Files\mineLogger\` (or your AppData if you
  choose the per-user option in the installer dialog)
- Creates a Start Menu shortcut
- Optionally registers the server to start silently at login (checkbox is ticked by
  default — uncheck if you prefer to start it manually)

No Python installation is required. Everything is bundled.

After installation, use the Start Menu shortcut or navigate to
`http://localhost:5000` in your browser. If autostart is enabled, the server will
be running automatically after each login.

**Uninstalling** via *Add or Remove Programs* removes the application and the
autostart entry. Your data (`~/.minelogger/minelogger.db`) is not touched.

---

## From source

### Requirements

- Python 3.8 or newer
- pip

No external database or web server is required. The web UI runs a local
[Flask](https://flask.palletsprojects.com/) development server on your machine
(`localhost:5000` by default). It is not exposed to the network and is intended
for single-user local use only.

### Setup

```bash
# Clone the repo
git clone https://github.com/JaFRyd/mineLogger.git
cd mineLogger

# Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Web UI (recommended)

```bash
python main.py ui
```

Starts a local Flask server and opens your default browser to `http://localhost:5000`.
Press `Ctrl+C` to stop the server.

Optional: run on a different port:

```bash
python main.py ui --port 8080
```

### Command line

**Add an entry (interactive prompts):**
```bash
python main.py add
```

**Add an entry with flags:**
```bash
python main.py add --customer "Acme" --hours 3.5 --date 2026-02-19 "Fixed login bug"
```

**List all entries:**
```bash
python main.py list
```

**List with filters:**
```bash
python main.py list --today
python main.py list --from 2026-02-01 --to 2026-02-28
python main.py list --customer "Acme"
```

**Export to CSV:**
```bash
python main.py export --output february.csv --from 2026-02-01 --to 2026-02-28
```

---

## Autostart on Windows (from-source installs)

If you installed via the Windows Installer, autostart is handled for you. The
following applies only to from-source setups.

### Option A — Startup folder (simplest)

1. Create a file called `start-minelogger.vbs` anywhere convenient (e.g. the repo
   folder) with the following content — adjust the path to match your installation:

   ```vbscript
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run "cmd /c ""C:\Users\janne\Coding\mineLogger\.venv\Scripts\python.exe"" ""C:\Users\janne\Coding\mineLogger\main.py"" ui", 0, False
   ```

   The `0` as the third argument hides the console window so no terminal appears.

2. Press `Win + R`, type `shell:startup`, press Enter.

3. Place a shortcut to `start-minelogger.vbs` in the folder that opens.

The server will start silently at next login. To stop it, open Task Manager and
end the `python.exe` process.

### Option B — Task Scheduler (more control)

Task Scheduler lets you run the server at login, restart it on failure, and manage
it without touching startup folders.

1. Open **Task Scheduler** (search in Start menu).
2. Click **Create Basic Task** in the right panel.
3. Fill in the wizard:
   - **Name:** mineLogger
   - **Trigger:** When I log on
   - **Action:** Start a program
     - **Program:** `C:\Users\janne\Coding\mineLogger\.venv\Scripts\python.exe`
     - **Arguments:** `main.py ui`
     - **Start in:** `C:\Users\janne\Coding\mineLogger`
4. Finish the wizard.
5. Find the task in the list, open its **Properties**, go to the **General** tab,
   and tick **Run only when user is logged on** and **Hidden**.

To stop or disable the server, right-click the task and choose **End** or **Disable**.

> **Note:** Both options start the server without opening the browser automatically.
> Just navigate to `http://localhost:5000` yourself after login.

---

## Building the Windows Installer

Requires [PyInstaller](https://pyinstaller.org/) and
[Inno Setup 6](https://jrsoftware.org/isinfo.php) installed on the build machine.

```bat
pip install pyinstaller
build.bat 1.0.0
```

The installer is written to `installer_output\minelogger-setup.exe`.

---

## Data storage

Entries are stored in a local SQLite database at:

```
~/.minelogger/minelogger.db
```

No data leaves your machine.
