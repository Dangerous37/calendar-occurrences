# Calendar Occurrences

Expand a recurring local booking into UTC occurrences for a downstream integration. Detect skipped and repeated wall times at daylight-saving transitions before exporting.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

Daily and weekly-style intervals only. This adapter accepts normalized booking JSON rather than arbitrary iCalendar rules. Requires IANA time zone data (on Windows run python -m pip install tzdata==2025.2 if the system has no database).

## Resumen en español

Expande citas recurrentes en su zona de origen y resuelve los cambios de horario de verano de manera explícita.
