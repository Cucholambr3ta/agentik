"""AGENTIK Hermes — Skills from successful sequences."""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Skill:
    """Skill data structure."""
    id: str
    name: str
    description: str
    steps: List[str]
    success_count: int = 0
    last_used: Optional[datetime] = None
    created: datetime = field(default_factory=datetime.now)


class SkillsManager:
    """Manage skills from successful sequences."""
    
    def __init__(self, storage_dir: str = "~/.agentik/skills"):
        self.storage_dir = os.path.expanduser(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)
        self._skills: List[Skill] = []
        self._load_skills()
    
    def _load_skills(self):
        """Load skills from storage."""
        skills_file = os.path.join(self.storage_dir, "skills.json")
        if os.path.exists(skills_file):
            try:
                with open(skills_file, 'r') as f:
                    data = json.load(f)
                    self._skills = [Skill(**item) for item in data]
            except Exception:
                self._skills = []
    
    def _save_skills(self):
        """Save skills to storage."""
        skills_file = os.path.join(self.storage_dir, "skills.json")
        with open(skills_file, 'w') as f:
            json.dump([{
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "steps": s.steps,
                "success_count": s.success_count,
                "last_used": s.last_used.isoformat() if s.last_used else None,
                "created": s.created.isoformat()
            } for s in self._skills], f, indent=2)
    
    def record_success(self, steps: List[str], name: Optional[str] = None) -> Skill:
        """Record a successful sequence and create/update skill."""
        # Check if similar skill exists
        existing = self._find_similar(steps)
        
        if existing:
            existing.success_count += 1
            existing.last_used = datetime.now()
            self._save_skills()
            return existing
        
        # Create new skill
        skill = Skill(
            id=f"skill-{datetime.now().timestamp()}",
            name=name or f"Skill from {len(self._skills) + 1} steps",
            description=f"Skill learned from {len(steps)} successful steps",
            steps=steps,
            success_count=1,
            last_used=datetime.now()
        )
        
        self._skills.append(skill)
        self._save_skills()
        return skill
    
    def _find_similar(self, steps: List[str]) -> Optional[Skill]:
        """Find similar skill by steps."""
        for skill in self._skills:
            if skill.steps == steps:
                return skill
        return None
    
    def get_skills(self) -> List[Skill]:
        """Get all skills."""
        return self._skills.copy()
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        for skill in self._skills:
            if skill.id == skill_id:
                return skill
        return None
    
    def get_popular_skills(self, min_successes: int = 3) -> List[Skill]:
        """Get popular skills with many successes."""
        return [s for s in self._skills if s.success_count >= min_successes]


# Global skills manager instance
skills_manager = SkillsManager()
