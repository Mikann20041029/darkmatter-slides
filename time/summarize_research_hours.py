#!/usr/bin/env python3

import csv
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys


START_DATE = date(2026, 4, 1)
END_DATE = date(2027, 3, 31)
CSV_PATH = Path(__file__).with_name("research_hours_2026.csv")
FIELDNAMES = ["date", "on_campus_hours", "off_campus_hours", "note"]


def expected_dates():
    cur = START_DATE
    while cur <= END_DATE:
        yield cur
        cur += timedelta(days=1)


def parse_hours(raw_value, line_no):
    value = raw_value.strip()
    if value == "":
        return Decimal("0")
    try:
        hours = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"line {line_no}: invalid hours value: {raw_value!r}") from exc
    if hours < 0:
        raise ValueError(f"line {line_no}: hours must be non-negative: {raw_value!r}")
    return hours


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError(
                "header must be exactly: date,on_campus_hours,off_campus_hours,note"
            )

        rows = {}
        for line_no, row in enumerate(reader, start=2):
            raw_date = (row.get("date") or "").strip()
            if raw_date == "":
                raise ValueError(f"line {line_no}: date is required")
            try:
                parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except ValueError as exc:
                raise ValueError(
                    f"line {line_no}: invalid date format: {raw_date!r}"
                ) from exc

            if not (START_DATE <= parsed_date <= END_DATE):
                raise ValueError(
                    f"line {line_no}: date out of range: {raw_date!r}"
                )
            if parsed_date in rows:
                raise ValueError(
                    f"line {line_no}: duplicate date found: {raw_date!r}"
                )

            rows[parsed_date] = {
                "on_campus_hours": parse_hours(
                    row.get("on_campus_hours") or "", line_no
                ),
                "off_campus_hours": parse_hours(
                    row.get("off_campus_hours") or "", line_no
                ),
            }

        return rows


def validate_dates(rows):
    missing = [day.isoformat() for day in expected_dates() if day not in rows]
    if missing:
        preview = ", ".join(missing[:5])
        suffix = " ..." if len(missing) > 5 else ""
        raise ValueError(f"missing dates: {preview}{suffix}")


def summarize(rows):
    monthly = defaultdict(
        lambda: {
            "on_campus_hours": Decimal("0"),
            "off_campus_hours": Decimal("0"),
            "total_hours": Decimal("0"),
        }
    )
    totals = {
        "on_campus_hours": Decimal("0"),
        "off_campus_hours": Decimal("0"),
        "total_hours": Decimal("0"),
    }

    for day in expected_dates():
        hours = rows[day]
        day_total = hours["on_campus_hours"] + hours["off_campus_hours"]
        key = day.strftime("%Y-%m")
        monthly[key]["on_campus_hours"] += hours["on_campus_hours"]
        monthly[key]["off_campus_hours"] += hours["off_campus_hours"]
        monthly[key]["total_hours"] += day_total
        totals["on_campus_hours"] += hours["on_campus_hours"]
        totals["off_campus_hours"] += hours["off_campus_hours"]
        totals["total_hours"] += day_total

    return monthly, totals


def main():
    rows = load_rows(CSV_PATH)
    validate_dates(rows)
    monthly, totals = summarize(rows)

    print(f"file: {CSV_PATH}")
    print("")
    print("monthly research hours")
    print("month,on_campus_hours,off_campus_hours,total_hours")
    for month in sorted(monthly):
        values = monthly[month]
        print(
            f"{month},{values['on_campus_hours']},"
            f"{values['off_campus_hours']},{values['total_hours']}"
        )
    print("")
    print(
        "total,"
        f"{totals['on_campus_hours']},"
        f"{totals['off_campus_hours']},"
        f"{totals['total_hours']}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
