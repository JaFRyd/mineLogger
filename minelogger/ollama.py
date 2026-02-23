import json
import re
from datetime import date

import requests

MODEL = "llama3.2"
_API_URL = "http://localhost:11434/api/chat"

_SYSTEM_PROMPT_TEMPLATE = """\
You are a work-log entry extractor.
Today's date is {today}.
Known customers: {customers}. Match to this list if similar; otherwise use as spoken.

Extract the four fields and return ONLY valid JSON — no fences, no explanation:
{{"date": "YYYY-MM-DD", "customer": "...", "hours": <float>, "description": "..."}}

Rules:
- date: use mentioned date; default to today if none
- hours: "two hours"=2.0, "half a day"=4.0, "30 minutes"=0.5, "an hour and a half"=1.5
- description: concise task summary — do NOT repeat customer name or hours\
"""


class OllamaError(Exception):
    pass


def _strip_fences(text: str) -> str:
    """Remove accidental ``` or ```json wrappers from model output."""
    text = text.strip()
    text = re.sub(r"^```[a-z]*\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_entry(message: str, customers: list) -> dict:
    """Call local Ollama to extract structured work-log fields from free text.

    Returns a dict with keys: date, customer, hours, description.
    Raises OllamaError on any failure.
    """
    today = date.today().isoformat()
    customer_list = ", ".join(customers) if customers else "(none)"
    system_prompt = _SYSTEM_PROMPT_TEMPLATE.format(today=today, customers=customer_list)

    payload = {
        "model": MODEL,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    }

    try:
        resp = requests.post(_API_URL, json=payload, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise OllamaError(
            "Cannot reach Ollama. Is it running? Try: ollama serve"
        )
    except requests.exceptions.Timeout:
        raise OllamaError("Ollama request timed out after 30 s.")
    except requests.exceptions.HTTPError as exc:
        raise OllamaError(f"Ollama returned HTTP {exc.response.status_code}.")

    try:
        body = resp.json()
        raw = body["message"]["content"]
    except (KeyError, ValueError) as exc:
        raise OllamaError(f"Unexpected response from Ollama: {exc}")

    cleaned = _strip_fences(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise OllamaError(f"Model returned invalid JSON: {exc}\n\nRaw output:\n{raw}")

    for field in ("date", "customer", "hours", "description"):
        if field not in data:
            raise OllamaError(f"Model response missing field: '{field}'")

    try:
        data["hours"] = float(data["hours"])
    except (TypeError, ValueError):
        raise OllamaError(f"Model returned non-numeric hours: {data['hours']!r}")

    if data["hours"] <= 0:
        raise OllamaError(f"Model returned non-positive hours: {data['hours']}")

    return data
