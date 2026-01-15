#!/usr/bin/env python3
"""
Felix Learning Platform - Study Planner
Generates personalized study plans based on goals and available time
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta


@dataclass
class StudyBlock:
    """A block of study time"""
    phase: int
    lesson: str
    duration_hours: float
    priority: int
    topics: List[str]


class FelixStudyPlanner:
    """Creates personalized study plans"""

    def __init__(self):
        self.phase_topics = {
            0: ["Setup", "Environment", "Tooling"],
            1: ["Linear Algebra", "Calculus", "Probability", "Statistics", "Optimization"],
            2: ["Supervised Learning", "Unsupervised Learning", "Ensemble Methods"],
            3: ["Neural Networks", "Backpropagation", "Training", "Frameworks"],
            4: ["CNNs", "Object Detection", "Segmentation", "Generation"],
            5: ["Tokenization", "Embeddings", "Attention", "Transformers"],
            6: ["Speech", "Audio", "TTS", "ASR"],
            7: ["Architecture", "Training", "Fine-tuning"],
            8: ["Agents", "Memory", "Planning"],
            9: ["RL", "Policy", "Value Functions"],
            10: ["LLMs", "RLHF", "Alignment"],
            11: ["RAG", "Agents", "Production"],
            12: ["Vision", "Language", "Audio"],
            13: ["MCP", "Tools", "APIs"],
            14: ["Agent Loops", "Tool Use", "Memory"],
            15: ["Autonomous", "Safety", "Monitoring"],
            16: ["Multi-Agent", "Coordination", "Swarms"],
            17: ["Deployment", "Scaling", "Monitoring"],
            18: ["Ethics", "Safety", "Fairness"],
            19: ["Capstone", "Integration", "Portfolio"]
        }

    def generate_plan(
        self,
        weekly_hours: float,
        weeks: int,
        target_phase: Optional[int] = None,
        focus_topics: Optional[List[str]] = None
    ) -> List[StudyBlock]:
        """Generate a study plan"""
        plan = []
        available_hours = weekly_hours * weeks

        # Determine phases to cover
        if target_phase:
            phases_to_cover = list(range(target_phase + 1))
        else:
            phases_to_cover = list(range(20))

        # Filter by focus topics if specified
        if focus_topics:
            phases_to_cover = self._filter_by_topics(phases_to_cover, focus_topics)

        # Generate study blocks
        current_week = 1
        hours_remaining = available_hours

        for phase_id in phases_to_cover:
            if hours_remaining <= 0:
                break

            phase_hours = self._estimate_phase_hours(phase_id)
            if phase_hours > hours_remaining:
                # Partial phase
                lessons_to_cover = int((hours_remaining / phase_hours) * 10)
            else:
                lessons_to_cover = 10

            for lesson_num in range(lessons_to_cover):
                if hours_remaining <= 0:
                    break

                block = StudyBlock(
                    phase=phase_id,
                    lesson=self._get_lesson_name(phase_id, lesson_num),
                    duration_hours=min(hours_remaining / lessons_to_cover, 2),
                    priority=self._calculate_priority(phase_id, focus_topics),
                    topics=self.phase_topics.get(phase_id, [])
                )
                plan.append(block)
                hours_remaining -= block.duration_hours

        return plan

    def _filter_by_topics(self, phases: List[int], topics: List[str]) -> List[int]:
        """Filter phases by relevant topics"""
        filtered = []
        for phase_id in phases:
            phase_topics = self.phase_topics.get(phase_id, [])
            if any(topic.lower() in ' '.join(phase_topics).lower() for topic in topics):
                filtered.append(phase_id)
        return filtered if filtered else phases

    def _estimate_phase_hours(self, phase_id: int) -> float:
        """Estimate hours for a phase"""
        hours_map = {
            0: 20, 1: 40, 2: 35, 3: 30, 4: 45,
            5: 35, 6: 25, 7: 30, 8: 35, 9: 30,
            10: 45, 11: 30, 12: 30, 13: 20, 14: 35,
            15: 30, 16: 35, 17: 25, 18: 15, 19: 40
        }
        return hours_map.get(phase_id, 30)

    def _get_lesson_name(self, phase_id: int, lesson_num: int) -> str:
        """Get a lesson name"""
        lesson_templates = {
            0: ["Environment Setup", "Git Basics", "Python Setup", "Jupyter", "Docker"],
            1: ["Linear Algebra", "Vectors", "Matrices", "Calculus", "Probability"],
            2: ["Linear Regression", "Logistic Regression", "Trees", "SVM", "Ensemble"],
            3: ["Perceptron", "MLP", "Backprop", "Training", "Frameworks"],
        }
        return lesson_templates.get(phase_id, ["Lesson"])[lesson_num % 5]

    def _calculate_priority(self, phase_id: int, focus_topics: Optional[List[str]]) -> int:
        """Calculate lesson priority (1 = highest)"""
        base_priority = phase_id + 1
        if focus_topics:
            phase_topics = self.phase_topics.get(phase_id, [])
            for topic in focus_topics:
                if topic.lower() in ' '.join(phase_topics).lower():
                    return max(1, base_priority - 3)
        return base_priority

    def print_plan(self, plan: List[StudyBlock], weekly_hours: float):
        """Print a formatted study plan"""
        print("\n" + "=" * 70)
        print("  FELIX PERSONALIZED STUDY PLAN")
        print("=" * 70)

        current_week = 1
        hours_this_week = 0
        week_limit = weekly_hours

        print(f"\n📅 Duration: {len(plan) * 2 / weekly_hours:.1f} weeks")
        print(f"⏱️  Weekly commitment: {weekly_hours} hours")
        print(f"📚 Total lessons planned: {len(plan)}\n")

        for i, block in enumerate(plan):
            hours_this_week += block.duration_hours

            if hours_this_week > week_limit:
                current_week += 1
                hours_this_week = block.duration_hours
                print(f"\n{'─' * 70}")
                print(f"📆 WEEK {current_week}")
                print(f"{'─' * 70}")

            print(f"   Week {current_week} | Phase {block.phase} | {block.duration_hours:.1f}h")
            print(f"   📖 {block.lesson}")
            print(f"   🏷️  Topics: {', '.join(block.topics[:3])}")
            print()

        print("=" * 70)
        print(f"✅ Plan generated: {len(plan)} lessons across {current_week} weeks")
        print("=" * 70 + "\n")

    def export_to_json(self, plan: List[StudyBlock], path: str = "study-plan.json"):
        """Export plan to JSON"""
        plan_data = {
            "generated_at": datetime.now().isoformat(),
            "total_lessons": len(plan),
            "estimated_hours": sum(b.duration_hours for b in plan),
            "phases_covered": len(set(b.phase for b in plan)),
            "plan": [
                {
                    "phase": b.phase,
                    "lesson": b.lesson,
                    "duration_hours": b.duration_hours,
                    "priority": b.priority,
                    "topics": b.topics
                }
                for b in plan
            ]
        }
        with open(path, 'w') as f:
            json.dump(plan_data, f, indent=2)
        print(f"✅ Study plan exported to: {path}")


def main():
    planner = FelixStudyPlanner()

    # Generate a sample plan
    plan = planner.generate_plan(
        weekly_hours=10,
        weeks=12,
        focus_topics=["Deep Learning", "Agents"]
    )

    planner.print_plan(plan, weekly_hours=10)
    planner.export_to_json(plan)


if __name__ == "__main__":
    main()