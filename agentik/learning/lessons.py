"""AGENTIK Hermes — Lessons from repeated failures."""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Lesson:
    """Lesson data structure."""
    id: str
    title: str
    description: str
    category: str
    trigger: str
    solution: str
    occurrences: int = 1
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


class LessonsManager:
    """Manage lessons from repeated failures."""
    
    def __init__(self, storage_dir: str = "~/.agentik/lessons"):
        self.storage_dir = os.path.expanduser(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)
        self._lessons: List[Lesson] = []
        self._load_lessons()
    
    def _load_lessons(self):
        """Load lessons from storage."""
        lessons_file = os.path.join(self.storage_dir, "lessons.json")
        if os.path.exists(lessons_file):
            try:
                with open(lessons_file, 'r') as f:
                    data = json.load(f)
                    self._lessons = [Lesson(**item) for item in data]
            except Exception:
                self._lessons = []
    
    def _save_lessons(self):
        """Save lessons to storage."""
        lessons_file = os.path.join(self.storage_dir, "lessons.json")
        with open(lessons_file, 'w') as f:
            json.dump([{
                "id": l.id,
                "title": l.title,
                "description": l.description,
                "category": l.category,
                "trigger": l.trigger,
                "solution": l.solution,
                "occurrences": l.occurrences,
                "first_seen": l.first_seen.isoformat(),
                "last_seen": l.last_seen.isoformat()
            } for l in self._lessons], f, indent=2)
    
    def record_failure(self, trigger: str, category: str = "general") -> Optional[Lesson]:
        """Record a failure and create/update lesson."""
        # Check if similar lesson exists
        existing = self._find_similar(trigger)
        
        if existing:
            existing.occurrences += 1
            existing.last_seen = datetime.now()
            self._save_lessons()
            return existing
        
        # Create new lesson
        lesson = Lesson(
            id=f"lesson-{datetime.now().timestamp()}",
            title=f"Lesson from: {trigger[:50]}",
            description=f"Lesson learned from repeated failure: {trigger}",
            category=category,
            trigger=trigger,
            solution="Manual review required"
        )
        
        self._lessons.append(lesson)
        self._save_lessons()
        return lesson
    
    def _find_similar(self, trigger: str) -> Optional[Lesson]:
        """Find similar lesson by trigger."""
        for lesson in self._lessons:
            if lesson.trigger == trigger:
                return lesson
        return None
    
    def get_lessons(self, category: Optional[str] = None) -> List[Lesson]:
        """Get lessons, optionally filtered by category."""
        if category:
            return [l for l in self._lessons if l.category == category]
        return self._lessons.copy()
    
    def get_repeated_failures(self, min_occurrences: int = 2) -> List[Lesson]:
        """Get lessons with repeated failures."""
        return [l for l in self._lessons if l.occurrences >= min_occurrences]


# Global lessons manager instance
lessons_manager = LessonsManager()
