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

## Requirements

- Python 3.8 or newer
- pip

No external database or web server is required. The web UI runs a local
[Flask](https://flask.palletsprojects.com/) development server on your machine
(`localhost:5000` by default). It is not exposed to the network and is intended
for single-user local use only.

---

## Installation

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

## Data storage

Entries are stored in a local SQLite database at:

```
~/.minelogger/minelogger.db
```

No data leaves your machine.
