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
