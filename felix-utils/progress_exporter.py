#!/usr/bin/env python3
"""
Felix Learning Platform - Progress Exporter
Reads localStorage-based progress data (exported as JSON) and
produces human-readable reports, CSV exports, and streak analysis.

Usage:
    python progress_exporter.py --input progress.json --format csv
    python progress_exporter.py --input progress.json --format report
    python progress_exporter.py --input progress.json --format streaks
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional


PHASE_NAMES = {
    0: "Setup & Tooling",
    1: "Math Foundations",
    2: "ML Fundamentals",
    3: "Deep Learning Core",
    4: "Computer Vision",
    5: "NLP: Foundations to Advanced",
    6: "Speech & Audio",
    7: "Transformers Deep Dive",
    8: "Generative AI",
    9: "Reinforcement Learning",
    10: "LLMs from Scratch",
    11: "LLM Engineering",
    12: "Multimodal AI",
    13: "Tools & Protocols",
    14: "Agent Engineering",
    15: "Autonomous Systems",
    16: "Multi-Agent & Swarms",
    17: "Infrastructure & Production",
    18: "Ethics, Safety & Alignment",
    19: "Capstone Projects",
}


@dataclass
class LessonRecord:
    path: str
    phase_id: int
    phase_name: str
    lesson_slug: str
    completed: bool
    completed_at: Optional[date]


@dataclass
class StreakInfo:
    current_streak: int
    longest_streak: int
    last_active: Optional[date]
    total_active_days: int


def parse_progress_json(data: dict) -> List[LessonRecord]:
    """Parse Felix progress JSON (format: {path: timestamp | boolean})"""
    records = []
    for path, value in data.items():
        parts = path.split("/")
        if len(parts) < 3 or parts[0] != "phases":
            continue

        phase_slug = parts[1]
        lesson_slug = parts[2] if len(parts) > 2 else ""

        try:
            phase_id = int(phase_slug.split("-")[0])
        except (ValueError, IndexError):
            phase_id = -1

        phase_name = PHASE_NAMES.get(phase_id, phase_slug)

        completed_at = None
        completed = False

        if isinstance(value, bool):
            completed = value
        elif isinstance(value, (int, float)):
            completed = True
            try:
                completed_at = datetime.fromtimestamp(value / 1000).date()
            except (OSError, OverflowError):
                pass
        elif isinstance(value, str):
            completed = True
            try:
                completed_at = datetime.fromisoformat(value).date()
            except ValueError:
                pass

        records.append(LessonRecord(
            path=path,
            phase_id=phase_id,
            phase_name=phase_name,
            lesson_slug=lesson_slug,
            completed=completed,
            completed_at=completed_at,
        ))

    return sorted(records, key=lambda r: (r.phase_id, r.lesson_slug))


def compute_streaks(records: List[LessonRecord]) -> StreakInfo:
    """Compute current and longest study streak from completion dates."""
    dates = {r.completed_at for r in records if r.completed and r.completed_at}
    if not dates:
        return StreakInfo(0, 0, None, 0)

    sorted_dates = sorted(dates)
    today = date.today()

    # Current streak
    current = 0
    check = today
    while check in dates:
        current += 1
        check -= timedelta(days=1)

    # Also check if streak ends yesterday (common for timezones)
    if current == 0:
        check = today - timedelta(days=1)
        while check in dates:
            current += 1
            check -= timedelta(days=1)

    # Longest streak
    longest = 1
    run = 1
    for i in range(1, len(sorted_dates)):
        delta = (sorted_dates[i] - sorted_dates[i - 1]).days
        if delta == 1:
            run += 1
            longest = max(longest, run)
        elif delta > 1:
            run = 1

    return StreakInfo(
        current_streak=current,
        longest_streak=longest,
        last_active=sorted_dates[-1],
        total_active_days=len(dates),
    )


def export_csv(records: List[LessonRecord], output_path: Path) -> None:
    fieldnames = ["path", "phase_id", "phase_name", "lesson_slug", "completed", "completed_at"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = asdict(r)
            row["completed_at"] = str(r.completed_at) if r.completed_at else ""
            writer.writerow(row)
    print(f"CSV exported to {output_path}")


def print_report(records: List[LessonRecord]) -> None:
    completed = [r for r in records if r.completed]
    streaks = compute_streaks(records)

    phase_stats: Dict[int, dict] = {}
    for r in records:
        if r.phase_id not in phase_stats:
            phase_stats[r.phase_id] = {"name": r.phase_name, "total": 0, "done": 0}
        phase_stats[r.phase_id]["total"] += 1
        if r.completed:
            phase_stats[r.phase_id]["done"] += 1

    print("\n" + "=" * 56)
    print("  FELIX LEARNING PROGRESS REPORT")
    print(f"  Generated: {date.today()}")
    print("=" * 56)
    print(f"  Total lessons tracked: {len(records)}")
    print(f"  Lessons completed:     {len(completed)}")
    pct = round(len(completed) / len(records) * 100, 1) if records else 0
    print(f"  Overall progress:      {pct}%")
    print(f"  Current streak:        {streaks.current_streak} day(s)")
    print(f"  Longest streak:        {streaks.longest_streak} day(s)")
    print(f"  Total active days:     {streaks.total_active_days}")
    if streaks.last_active:
        print(f"  Last active:           {streaks.last_active}")
    print("-" * 56)
    print("  PHASE BREAKDOWN")
    print("-" * 56)
    for pid in sorted(phase_stats.keys()):
        ps = phase_stats[pid]
        bar_pct = ps["done"] / ps["total"] if ps["total"] else 0
        bar = "█" * int(bar_pct * 20) + "░" * (20 - int(bar_pct * 20))
        print(f"  P{str(pid).zfill(2)} {ps['name'][:24]:<24} [{bar}] {ps['done']}/{ps['total']}")
    print("=" * 56 + "\n")


def print_streaks(records: List[LessonRecord]) -> None:
    streaks = compute_streaks(records)
    completed_with_dates = [r for r in records if r.completed and r.completed_at]
    by_date: Dict[date, List[str]] = {}
    for r in completed_with_dates:
        by_date.setdefault(r.completed_at, []).append(r.lesson_slug)

    print("\n  STREAK ANALYSIS")
    print("  " + "-" * 40)
    print(f"  Current streak: {streaks.current_streak} day(s)")
    print(f"  Longest streak: {streaks.longest_streak} day(s)")
    print(f"  Active days:    {streaks.total_active_days}")
    if streaks.last_active:
        gap = (date.today() - streaks.last_active).days
        print(f"  Days since last session: {gap}")

    if by_date:
        print("\n  RECENT ACTIVITY (last 14 days):")
        today = date.today()
        for delta in range(13, -1, -1):
            d = today - timedelta(days=delta)
            lessons = by_date.get(d, [])
            marker = "●" * min(len(lessons), 5) if lessons else "·"
            print(f"  {d}  {marker:5}  {len(lessons)} lesson(s)" if lessons else f"  {d}  {marker}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Felix Learning Progress Exporter")
    parser.add_argument("--input", "-i", required=True,
                        help="Path to progress JSON file (exported from Felix)")
    parser.add_argument("--format", "-f", choices=["csv", "report", "streaks"], default="report",
                        help="Output format")
    parser.add_argument("--output", "-o", help="Output file path (for CSV format)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {input_path}: {e}", file=sys.stderr)
            return 1

    records = parse_progress_json(raw)
    if not records:
        print("No valid progress records found.")
        return 0

    if args.format == "csv":
        output = Path(args.output) if args.output else input_path.with_suffix(".csv")
        export_csv(records, output)
    elif args.format == "streaks":
        print_streaks(records)
    else:
        print_report(records)

    return 0


if __name__ == "__main__":
    sys.exit(main())
