import click
from datetime import date
from . import db
from .export import generate_csv


@click.group()
def cli():
    """mineLogger — local work logger."""
    db.init_db()


@cli.command()
@click.option("--customer", default=None, help="Customer name")
@click.option("--hours", default=None, type=float, help="Hours worked")
@click.option("--date", "date_str", default=None, help="Date (YYYY-MM-DD), defaults to today")
@click.argument("description", default=None, required=False)
def add(customer, hours, date_str, description):
    """Add a new log entry."""
    if date_str is None:
        date_str = date.today().isoformat()

    if customer is None:
        customers = db.get_customers()
        hint = ""
        if customers:
            recent = ", ".join(customers[:5])
            hint = f" [{recent}]"
        customer = click.prompt(f"Customer{hint}")

    if hours is None:
        hours = click.prompt("Hours", type=float)

    if description is None:
        description = click.prompt("Description")

    db.add_entry(date_str, customer, hours, description)
    click.echo(f"Added: {date_str} | {customer} | {hours}h | {description}")


@cli.command(name="list")
@click.option("--today", is_flag=True, default=False, help="Show today's entries")
@click.option("--date", "date_str", default=None, help="Show entries for a specific date")
@click.option("--from", "date_from", default=None, help="Start date (YYYY-MM-DD)")
@click.option("--to", "date_to", default=None, help="End date (YYYY-MM-DD)")
@click.option("--customer", default=None, help="Filter by customer")
def list_entries(today, date_str, date_from, date_to, customer):
    """List log entries."""
    if today:
        date_str = date.today().isoformat()
    if date_str:
        date_from = date_str
        date_to = date_str

    entries = db.get_entries(date_from=date_from, date_to=date_to, customer=customer)

    if not entries:
        click.echo("No entries found.")
        return

    # Group by date
    by_date = {}
    for e in entries:
        by_date.setdefault(e["date"], []).append(e)

    total_all = 0.0
    for d in sorted(by_date.keys(), reverse=True):
        click.echo(d)
        day_total = 0.0
        for e in by_date[d]:
            click.echo(f"  {e['customer']:<20} {e['hours']:>5.1f}h  {e['description']}")
            day_total += e["hours"]
        click.echo(f"  {'-' * 40}")
        click.echo(f"  Total: {day_total:.1f}h")
        click.echo()
        total_all += day_total

    if len(by_date) > 1:
        click.echo(f"Grand total: {total_all:.1f}h")


@cli.command()
@click.option("--from", "date_from", default=None, help="Start date (YYYY-MM-DD)")
@click.option("--to", "date_to", default=None, help="End date (YYYY-MM-DD)")
@click.option("--customer", default=None, help="Filter by customer")
@click.option("--output", default="export.csv", help="Output filename", show_default=True)
def export(date_from, date_to, customer, output):
    """Export entries to CSV."""
    entries = db.get_entries(date_from=date_from, date_to=date_to, customer=customer)
    if not entries:
        click.echo("No entries to export.")
        return
    csv_data = generate_csv(entries)
    with open(output, "w", newline="", encoding="utf-8") as f:
        f.write(csv_data)
    click.echo(f"Exported {len(entries)} entries to {output}")


@cli.command()
@click.option("--port", default=5000, show_default=True, help="Port to listen on")
@click.option("--no-browser", "no_browser", is_flag=True, default=False,
              help="Start server without opening the browser (used for autostart).")
def ui(port, no_browser):
    """Start the web UI."""
    import logging, webbrowser, threading
    from pathlib import Path
    from .server import create_app

    # File logging — always write to ~/.minelogger/minelogger-server.log
    log_path = Path.home() / ".minelogger" / "minelogger-server.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(str(log_path), encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logging.getLogger("werkzeug").addHandler(handler)
    logging.getLogger("werkzeug").setLevel(logging.INFO)

    app = create_app()
    url = f"http://localhost:{port}"
    if not no_browser:
        def open_browser():
            import time
            time.sleep(1.5)
            webbrowser.open_new_tab(url)
        threading.Thread(target=open_browser, daemon=True).start()
    click.echo(f"Starting web UI at {url} — press Ctrl+C to stop")
    app.run(port=port, debug=False)
