#!/usr/bin/env python3
"""
Felix Learning Platform - Curriculum Management Utility
A comprehensive tool for managing and analyzing the learning curriculum
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class LessonMetadata:
    """Metadata for a single lesson"""
    phase_id: int
    phase_name: str
    lesson_name: str
    status: str
    languages: List[str]
    path: str
    difficulty: str
    estimated_hours: float


class FelixCurriculumManager:
    """Manages the Felix curriculum structure and provides utilities"""

    def __init__(self, base_path: str = "./public/phases"):
        self.base_path = Path(base_path)
        self.phase_order = [
            "00-setup-and-tooling",
            "01-math-foundations",
            "02-ml-fundamentals",
            "03-deep-learning-core",
            "04-computer-vision",
            "05-nlp-foundations-to-advanced",
            "06-speech-and-audio",
            "07-transformers-deep-dive",
            "08-generative-ai",
            "09-reinforcement-learning",
            "10-llms-from-scratch",
            "11-llm-engineering",
            "12-multimodal-ai",
            "13-tools-and-protocols",
            "14-agent-engineering",
            "15-autonomous-systems",
            "16-multi-agent-and-swarms",
            "17-infrastructure-and-production",
            "18-ethics-safety-and-alignment",
            "19-capstone-projects"
        ]

    def scan_curriculum(self) -> List[LessonMetadata]:
        """Scan the entire curriculum and extract metadata"""
        lessons = []

        for phase_id, phase_dir in enumerate(self.phase_order):
            phase_path = self.base_path / phase_dir
            if not phase_path.exists():
                continue

            phase_name = self._format_phase_name(phase_dir)

            for lesson_dir in phase_path.iterdir():
                if not lesson_dir.is_dir():
                    continue

                lesson_name = self._format_lesson_name(lesson_dir.name)
                languages = self._detect_languages(lesson_dir / "code")

                lesson = LessonMetadata(
                    phase_id=phase_id,
                    phase_name=phase_name,
                    lesson_name=lesson_name,
                    status="complete" if languages else "planned",
                    languages=languages,
                    path=str(lesson_dir),
                    difficulty=self._estimate_difficulty(phase_id),
                    estimated_hours=self._estimate_time(phase_id, bool(languages))
                )
                lessons.append(lesson)

        return lessons

    def _format_phase_name(self, phase_dir: str) -> str:
        """Convert directory name to human-readable phase name"""
        name = phase_dir.split("-", 2)[-1].replace("-", " ").title()
        return name

    def _format_lesson_name(self, lesson_dir: str) -> str:
        """Convert directory name to human-readable lesson name"""
        parts = lesson_dir.split("-", 2)
        if len(parts) >= 3:
            return parts[-1].replace("-", " ").title()
        return lesson_dir.replace("-", " ").title()

    def _detect_languages(self, code_dir: Path) -> List[str]:
        """Detect programming languages in a lesson"""
        languages = []
        if not code_dir.exists():
            return languages

        for file in code_dir.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                lang_map = {
                    '.py': 'Python',
                    '.ts': 'TypeScript',
                    '.tsx': 'TypeScript',
                    '.rs': 'Rust',
                    '.jl': 'Julia',
                    '.js': 'JavaScript',
                }
                if ext in lang_map and lang_map[ext] not in languages:
                    languages.append(lang_map[ext])

        return languages

    def _estimate_difficulty(self, phase_id: int) -> str:
        """Estimate difficulty based on phase number"""
        if phase_id <= 3:
            return "foundational"
        elif phase_id <= 7:
            return "intermediate"
        elif phase_id <= 14:
            return "advanced"
        return "expert"

    def _estimate_time(self, phase_id: int, has_code: bool) -> float:
        """Estimate learning time in hours"""
        base_times = {
            0: 2, 1: 4, 2: 3, 3: 5, 4: 4, 5: 3,
            6: 3, 7: 4, 8: 5, 9: 4, 10: 6,
            11: 3, 12: 4, 13: 3, 14: 5,
            15: 4, 16: 5, 17: 4, 18: 2, 19: 8
        }
        base = base_times.get(phase_id, 3)
        return base if has_code else base * 0.5

    def generate_curriculum_json(self, output_path: str = "curriculum.json"):
        """Generate a JSON dump of the entire curriculum"""
        lessons = self.scan_curriculum()
        curriculum = {
            "generated_at": datetime.now().isoformat(),
            "total_phases": 20,
            "total_lessons": len(lessons),
            "estimated_total_hours": sum(l.estimated_hours for l in lessons),
            "phases": self._group_by_phase(lessons),
            "lessons": [asdict(l) for l in lessons]
        }

        with open(output_path, 'w') as f:
            json.dump(curriculum, f, indent=2)
        print(f"✅ Curriculum JSON generated: {output_path}")

    def _group_by_phase(self, lessons: List[LessonMetadata]) -> Dict:
        """Group lessons by phase"""
        phases = {}
        for lesson in lessons:
            if lesson.phase_id not in phases:
                phases[lesson.phase_id] = {
                    "name": lesson.phase_name,
                    "lessons": [],
                    "total_hours": 0
                }
            phases[lesson.phase_id]["lessons"].append(lesson.lesson_name)
            phases[lesson.phase_id]["total_hours"] += lesson.estimated_hours
        return phases

    def print_summary(self):
        """Print a formatted summary of the curriculum"""
        lessons = self.scan_curriculum()

        print("\n" + "=" * 60)
        print("  FELIX LEARNING PLATFORM - CURRICULUM SUMMARY")
        print("=" * 60 + "\n")

        current_phase = -1
        for lesson in lessons:
            if lesson.phase_id != current_phase:
                print(f"\n📚 Phase {lesson.phase_id}: {lesson.phase_name}")
                print("-" * 40)
                current_phase = lesson.phase_id

            status_icon = "✅" if lesson.languages else "📋"
            langs = ", ".join(lesson.languages) if lesson.languages else "—"
            print(f"   {status_icon} {lesson.lesson_name}")
            print(f"      Languages: {langs} | Est: {lesson.estimated_hours:.1f}h | {lesson.difficulty}")

        print("\n" + "=" * 60)
        print(f"📊 Total: {len(lessons)} lessons across 20 phases")
        print(f"⏱️  Estimated: {sum(l.estimated_hours for l in lessons):.0f} hours")
        print("=" * 60 + "\n")


class FelixProgressTracker:
    """Tracks learning progress"""

    def __init__(self, save_path: str = ".felix-progress.json"):
        self.save_path = save_path
        self.progress = self._load_progress()

    def _load_progress(self) -> Dict:
        """Load progress from file"""
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                return json.load(f)
        return {"completed": [], "in_progress": {}, "notes": {}}

    def mark_complete(self, lesson_path: str):
        """Mark a lesson as complete"""
        if lesson_path not in self.progress["completed"]:
            self.progress["completed"].append(lesson_path)
        if lesson_path in self.progress["in_progress"]:
            del self.progress["in_progress"][lesson_path]
        self._save_progress()

    def mark_in_progress(self, lesson_path: str):
        """Mark a lesson as in progress"""
        if lesson_path not in self.progress["completed"]:
            self.progress["in_progress"][lesson_path] = datetime.now().isoformat()
        self._save_progress()

    def _save_progress(self):
        """Save progress to file"""
        with open(self.save_path, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def get_stats(self) -> Dict:
        """Get progress statistics"""
        return {
            "completed": len(self.progress["completed"]),
            "in_progress": len(self.progress["in_progress"]),
            "total_estimated_hours": len(self.progress["completed"]) * 3.5
        }


if __name__ == "__main__":
    manager = FelixCurriculumManager()

    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        manager.generate_curriculum_json()
    else:
        manager.print_summary()

    tracker = FelixProgressTracker()
    stats = tracker.get_stats()
    print(f"📈 Your Progress: {stats['completed']} completed, {stats['in_progress']} in progress")