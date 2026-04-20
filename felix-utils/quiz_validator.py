#!/usr/bin/env python3
"""
Felix Learning Platform - Quiz Validator
Scans all quiz.json files across phases and validates structure,
content quality, and coverage. Outputs a report with missing modules.
"""

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


REQUIRED_QUESTION_KEYS = {"stage", "question", "options", "correct", "explanation"}
VALID_STAGES = {"pre", "post"}
MIN_OPTIONS = 3
MAX_OPTIONS = 5
MIN_QUESTIONS = 3
MIN_EXPLANATION_CHARS = 30


@dataclass
class QuizIssue:
    phase: str
    module: str
    question_index: Optional[int]
    severity: str  # "error" | "warning"
    message: str


@dataclass
class ValidationReport:
    total_modules: int = 0
    modules_with_quiz: int = 0
    modules_missing_quiz: List[str] = field(default_factory=list)
    issues: List[QuizIssue] = field(default_factory=list)
    valid_quizzes: int = 0

    @property
    def coverage_pct(self) -> float:
        if self.total_modules == 0:
            return 0.0
        return round(self.modules_with_quiz / self.total_modules * 100, 1)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


def validate_question(q: dict, idx: int, phase: str, module: str) -> List[QuizIssue]:
    issues = []

    missing = REQUIRED_QUESTION_KEYS - set(q.keys())
    if missing:
        issues.append(QuizIssue(phase, module, idx, "error",
                                f"Missing keys: {missing}"))
        return issues

    if q["stage"] not in VALID_STAGES:
        issues.append(QuizIssue(phase, module, idx, "error",
                                f"Invalid stage '{q['stage']}' — must be 'pre' or 'post'"))

    if not isinstance(q["options"], list):
        issues.append(QuizIssue(phase, module, idx, "error",
                                "options must be a list"))
    elif not (MIN_OPTIONS <= len(q["options"]) <= MAX_OPTIONS):
        issues.append(QuizIssue(phase, module, idx, "warning",
                                f"Expected {MIN_OPTIONS}-{MAX_OPTIONS} options, got {len(q['options'])}"))

    if isinstance(q["options"], list):
        if not isinstance(q["correct"], int):
            issues.append(QuizIssue(phase, module, idx, "error",
                                    "'correct' must be an integer index"))
        elif not (0 <= q["correct"] < len(q["options"])):
            issues.append(QuizIssue(phase, module, idx, "error",
                                    f"'correct' index {q['correct']} out of range for {len(q['options'])} options"))

    if not isinstance(q.get("question", ""), str) or len(q.get("question", "")) < 10:
        issues.append(QuizIssue(phase, module, idx, "warning",
                                "Question text is too short"))

    explanation = q.get("explanation", "")
    if not isinstance(explanation, str) or len(explanation) < MIN_EXPLANATION_CHARS:
        issues.append(QuizIssue(phase, module, idx, "warning",
                                f"Explanation too short (<{MIN_EXPLANATION_CHARS} chars)"))

    return issues


def validate_quiz_file(quiz_path: Path, phase: str, module: str) -> tuple[bool, List[QuizIssue]]:
    issues = []
    try:
        with open(quiz_path) as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        return False, [QuizIssue(phase, module, None, "error", f"Invalid JSON: {e}")]
    except OSError as e:
        return False, [QuizIssue(phase, module, None, "error", f"Cannot read file: {e}")]

    if isinstance(raw, list):
        questions = raw
    elif isinstance(raw, dict) and isinstance(raw.get("questions"), list):
        questions = raw["questions"]
    else:
        return False, [QuizIssue(phase, module, None, "error",
                                 "Top-level must be a list or {questions: [...]}")]

    if len(questions) < MIN_QUESTIONS:
        issues.append(QuizIssue(phase, module, None, "warning",
                                f"Only {len(questions)} questions — recommend >= {MIN_QUESTIONS}"))

    for i, q in enumerate(questions):
        issues.extend(validate_question(q, i, phase, module))

    has_pre = any(q.get("stage") == "pre" for q in questions if isinstance(q, dict))
    has_post = any(q.get("stage") == "post" for q in questions if isinstance(q, dict))
    if not has_pre:
        issues.append(QuizIssue(phase, module, None, "warning", "No 'pre' stage questions"))
    if not has_post:
        issues.append(QuizIssue(phase, module, None, "warning", "No 'post' stage questions"))

    fatal = any(i.severity == "error" for i in issues)
    return not fatal, issues


def scan_phases_dir(phases_dir: Path) -> ValidationReport:
    report = ValidationReport()

    for phase_dir in sorted(phases_dir.iterdir()):
        if not phase_dir.is_dir():
            continue
        phase_name = phase_dir.name

        for module_dir in sorted(phase_dir.iterdir()):
            if not module_dir.is_dir():
                continue
            docs_file = module_dir / "docs" / "en.md"
            if not docs_file.exists():
                continue

            module_name = module_dir.name
            report.total_modules += 1

            quiz_file = module_dir / "quiz.json"
            if not quiz_file.exists():
                report.modules_missing_quiz.append(f"{phase_name}/{module_name}")
                continue

            report.modules_with_quiz += 1
            ok, issues = validate_quiz_file(quiz_file, phase_name, module_name)
            report.issues.extend(issues)
            if ok:
                report.valid_quizzes += 1

    return report


def print_report(report: ValidationReport) -> None:
    print("\n" + "=" * 60)
    print("  FELIX QUIZ VALIDATION REPORT")
    print("=" * 60)
    print(f"  Total modules with docs: {report.total_modules}")
    print(f"  Modules with quiz.json:  {report.modules_with_quiz}")
    print(f"  Coverage:                {report.coverage_pct}%")
    print(f"  Valid quizzes:           {report.valid_quizzes}")
    print(f"  Errors:                  {report.error_count}")
    print(f"  Warnings:                {report.warning_count}")
    print("=" * 60)

    if report.issues:
        print("\nISSUES:")
        for issue in report.issues:
            loc = f"{issue.phase}/{issue.module}"
            if issue.question_index is not None:
                loc += f" Q{issue.question_index + 1}"
            tag = "❌ ERROR  " if issue.severity == "error" else "⚠  WARNING"
            print(f"  {tag} [{loc}] {issue.message}")

    if report.modules_missing_quiz:
        print(f"\nMISSING QUIZ ({len(report.modules_missing_quiz)} modules):")
        for m in report.modules_missing_quiz[:20]:
            print(f"  • {m}")
        if len(report.modules_missing_quiz) > 20:
            print(f"  ... and {len(report.modules_missing_quiz) - 20} more")

    print()
    status = "✅ PASS" if report.error_count == 0 else "❌ FAIL"
    print(f"  Result: {status}")
    print("=" * 60 + "\n")


def main() -> int:
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    phases_dir = repo_root / "public" / "phases"

    if not phases_dir.exists():
        print(f"Error: phases directory not found at {phases_dir}", file=sys.stderr)
        return 1

    print(f"Scanning {phases_dir} ...")
    report = scan_phases_dir(phases_dir)
    print_report(report)

    return 0 if report.error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
