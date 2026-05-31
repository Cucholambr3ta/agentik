"""Tests for Hermes module."""

import pytest
import tempfile
import shutil
from agentik.learning.lessons import LessonsManager, Lesson
from agentik.learning.skills import SkillsManager, Skill


@pytest.fixture
def lessons_manager():
    """Create a temporary lessons manager."""
    temp_dir = tempfile.mkdtemp()
    manager = LessonsManager(storage_dir=temp_dir)
    yield manager
    shutil.rmtree(temp_dir)


@pytest.fixture
def skills_manager():
    """Create a temporary skills manager."""
    temp_dir = tempfile.mkdtemp()
    manager = SkillsManager(storage_dir=temp_dir)
    yield manager
    shutil.rmtree(temp_dir)


def test_lessons_record_failure(lessons_manager):
    """Test recording a failure."""
    lesson = lessons_manager.record_failure("test failure", "testing")
    assert lesson is not None
    assert lesson.occurrences == 1


def test_lessons_repeat_failure(lessons_manager):
    """Test recording repeated failures."""
    lessons_manager.record_failure("test failure", "testing")
    lesson = lessons_manager.record_failure("test failure", "testing")
    assert lesson.occurrences == 2


def test_lessons_get_lessons(lessons_manager):
    """Test getting lessons."""
    lessons_manager.record_failure("failure 1", "category1")
    lessons_manager.record_failure("failure 2", "category2")
    
    lessons = lessons_manager.get_lessons()
    assert len(lessons) == 2


def test_lessons_get_repeated(lessons_manager):
    """Test getting repeated failures."""
    lessons_manager.record_failure("failure 1", "testing")
    lessons_manager.record_failure("failure 1", "testing")
    lessons_manager.record_failure("failure 2", "testing")
    
    repeated = lessons_manager.get_repeated_failures(min_occurrences=2)
    assert len(repeated) == 1


def test_skills_record_success(skills_manager):
    """Test recording a success."""
    skill = skills_manager.record_success(["step1", "step2"], "test skill")
    assert skill is not None
    assert skill.success_count == 1


def test_skills_repeat_success(skills_manager):
    """Test recording repeated successes."""
    skills_manager.record_success(["step1", "step2"], "test skill")
    skill = skills_manager.record_success(["step1", "step2"], "test skill")
    assert skill.success_count == 2


def test_skills_get_skills(skills_manager):
    """Test getting skills."""
    skills_manager.record_success(["step1", "step2"], "skill 1")
    skills_manager.record_success(["step3", "step4"], "skill 2")
    
    skills = skills_manager.get_skills()
    assert len(skills) == 2


def test_skills_get_popular(skills_manager):
    """Test getting popular skills."""
    for _ in range(3):
        skills_manager.record_success(["step1", "step2"], "popular skill")
    skills_manager.record_success(["step3", "step4"], "new skill")
    
    popular = skills_manager.get_popular_skills(min_successes=3)
    assert len(popular) == 1
