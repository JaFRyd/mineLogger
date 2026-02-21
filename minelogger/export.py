import csv
import io


def generate_csv(entries):
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["date", "customer", "hours", "description", "created_at"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(entries)
    return output.getvalue()


def parse_csv(text):
    """Parse CSV text into row dicts. Returns (rows, errors)."""
    rows = []
    errors = []
    try:
        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames is None:
            return [], ["The file appears to be empty."]
        required = {"date", "customer", "hours", "description"}
        missing_cols = required - {f.strip().lower() for f in reader.fieldnames}
        if missing_cols:
            return [], [f"Missing required columns: {', '.join(sorted(missing_cols))}"]
        for i, row in enumerate(reader, start=2):
            date = row.get("date", "").strip()
            customer = row.get("customer", "").strip()
            description = row.get("description", "").strip()
            if not date or not customer or not description:
                errors.append(f"Row {i}: date, customer, and description are required.")
                continue
            try:
                hours = float(row.get("hours", ""))
                if hours <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                errors.append(f"Row {i}: invalid hours value '{row.get('hours')}'.")
                continue
            rows.append({
                "date": date,
                "customer": customer,
                "hours": hours,
                "description": description,
                "created_at": row.get("created_at", "").strip(),
            })
    except Exception as e:
        return [], [f"Could not parse CSV: {e}"]
    return rows, errors
