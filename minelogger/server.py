from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from datetime import date
from . import db
from .export import generate_csv, parse_csv


def create_app():
    import os, sys
    if getattr(sys, "frozen", False):
        template_dir = os.path.join(sys._MEIPASS, "minelogger", "templates")
    else:
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "minelogger-secret"

    db.init_db()

    @app.route("/")
    def index():
        return redirect(url_for("add_entry"))

    @app.route("/add", methods=["GET", "POST"])
    def add_entry():
        if request.method == "POST":
            date_str = request.form.get("date") or date.today().isoformat()
            customer = request.form.get("customer", "").strip()
            hours = request.form.get("hours", "")
            description = request.form.get("description", "").strip()

            errors = []
            if not customer:
                errors.append("Customer is required.")
            if not description:
                errors.append("Description is required.")
            try:
                hours = float(hours)
                if hours <= 0:
                    errors.append("Hours must be positive.")
            except (ValueError, TypeError):
                errors.append("Hours must be a number.")

            if errors:
                for e in errors:
                    flash(e, "error")
            else:
                db.add_entry(date_str, customer, hours, description)
                flash("Entry added.", "success")
                return redirect(url_for("add_entry"))

        customers = db.get_managed_customers()
        today = date.today().isoformat()
        return render_template("add.html", customers=customers, today=today, active="add")

    @app.route("/log")
    def view_log():
        import calendar
        month = request.args.get("month") or None
        date_from = request.args.get("date_from") or None
        date_to = request.args.get("date_to") or None
        customer = request.args.get("customer") or None

        # When a month is selected and no explicit date range, derive it
        if month and not date_from and not date_to:
            year, mon = int(month.split("-")[0]), int(month.split("-")[1])
            date_from = f"{year:04d}-{mon:02d}-01"
            last_day = calendar.monthrange(year, mon)[1]
            date_to = f"{year:04d}-{mon:02d}-{last_day:02d}"

        entries = db.get_entries(date_from=date_from, date_to=date_to, customer=customer)
        customers = db.get_customers()
        total = sum(e["hours"] for e in entries)
        months = db.get_months()
        summary = db.get_monthly_summary(month) if month else []
        return render_template(
            "log.html",
            entries=entries,
            customers=customers,
            total=total,
            date_from=date_from or "",
            date_to=date_to or "",
            selected_customer=customer or "",
            active="log",
            months=months,
            selected_month=month or "",
            summary=summary,
        )

    @app.route("/export", methods=["GET", "POST"])
    def export():
        customers = db.get_customers()
        if request.method == "POST":
            date_from = request.form.get("date_from") or None
            date_to = request.form.get("date_to") or None
            customer = request.form.get("customer") or None
            filename = request.form.get("filename", "export").strip() or "export"
            if not filename.endswith(".csv"):
                filename += ".csv"

            entries = db.get_entries(date_from=date_from, date_to=date_to, customer=customer)
            csv_data = generate_csv(entries)
            response = make_response(csv_data)
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            response.headers["Content-Type"] = "text/csv"
            return response

        return render_template("export.html", customers=customers, active="export")

    @app.route("/import", methods=["POST"])
    def import_csv():
        f = request.files.get("csv_file")
        if not f or not f.filename:
            flash("Please select a CSV file.", "error")
            return redirect(url_for("export"))
        try:
            text = f.read().decode("utf-8-sig")  # utf-8-sig strips BOM if present
        except UnicodeDecodeError:
            flash("File must be UTF-8 encoded.", "error")
            return redirect(url_for("export"))
        rows, errors = parse_csv(text)
        for e in errors:
            flash(e, "error")
        if rows:
            imported, skipped = db.import_entries(rows)
            if imported:
                flash(f"Imported {imported} entr{'y' if imported == 1 else 'ies'}.", "success")
            if skipped:
                flash(f"Skipped {skipped} duplicate entr{'y' if skipped == 1 else 'ies'}.", "success")
        elif not errors:
            flash("The CSV file was empty.", "error")
        return redirect(url_for("export"))

    @app.route("/customers", methods=["GET", "POST"])
    def manage_customers():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if name:
                db.add_customer(name)
                flash(f'Customer "{name}" added.', "success")
            else:
                flash("Customer name cannot be empty.", "error")
            return redirect(url_for("manage_customers"))
        customers = db.get_managed_customers()
        return render_template("customers.html", customers=customers, active="customers")

    @app.route("/customers/<path:name>/delete", methods=["POST"])
    def delete_customer(name):
        db.remove_customer(name)
        flash(f'Customer "{name}" removed from preselection.', "success")
        return redirect(url_for("manage_customers"))

    @app.route("/entry/<int:entry_id>/delete", methods=["POST"])
    def delete_entry(entry_id):
        db.delete_entry(entry_id)
        flash("Entry deleted.", "success")
        # Return to log with previous filters preserved
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        return redirect(url_for("view_log"))

    return app
