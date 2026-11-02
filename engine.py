from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def evaluate(data):
    start = datetime.fromisoformat(data["start"])
    zone = ZoneInfo(data["zone"])
    if start.tzinfo is not None:
        raise ValueError("start must be a local timestamp")
    step, count = data["interval_days"], data["count"]
    if type(step) is not int or step < 1 or type(count) is not int or not 1 <= count <= 10000:
        raise ValueError("invalid interval or count")
    choice = data.get("ambiguous", "earlier")
    if choice not in ("earlier","later"):
        raise ValueError("invalid ambiguous-time policy")
    exclude = set(data.get("exclude", []))
    rows = []
    for i in range(count):
        wall = start + timedelta(days=step*i)
        row = {"local": wall.isoformat()}
        options = set()
        for fold in (0,1):
            utc = wall.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
            if utc.astimezone(zone).replace(tzinfo=None) == wall:
                options.add(utc)
        if wall.date().isoformat() in exclude:
            row["status"] = "excluded"
        elif not options:
            row["status"] = "nonexistent"
        else:
            instant = min(options) if choice == "earlier" else max(options)
            row.update(status="scheduled", utc=instant.isoformat(),
                       offset=str(instant.astimezone(zone).utcoffset()), ambiguous=len(options)>1)
        rows.append(row)
    return rows
