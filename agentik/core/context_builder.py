"""AGENTIK Context Builder — Pipeline de contexto según especificación."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

try:
    from agentik.mempalace.searcher import Searcher
    from agentik.mempalace.config import MempalaceConfig
    _MEMPALACE_AVAILABLE = True
except ImportError:
    _MEMPALACE_AVAILABLE = False


@dataclass
class Context:
    """Context data structure."""
    user_input: str
    conversation: List[Dict[str, Any]] = field(default_factory=list)
    memories: List[Dict[str, Any]] = field(default_factory=list)
    lessons: List[Dict[str, Any]] = field(default_factory=list)
    skills: List[Dict[str, Any]] = field(default_factory=list)
    security_policies: List[Dict[str, Any]] = field(default_factory=list)
    final_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class ContextBuilder:
    """Pipeline de contexto según especificación.
    
    Input → Conversation → Memories → Lessons → Skills → Security Policies → Final Context
    
    Ningún módulo puede construir contexto por su cuenta (P4 del spec).
    """
    
    def __init__(self):
        self._conversation_history: List[Dict[str, Any]] = []
        self._searcher: Optional[Any] = None
        if _MEMPALACE_AVAILABLE:
            try:
                config = MempalaceConfig()
                self._searcher = Searcher(palace_path=config.palace_path)
            except Exception:
                self._searcher = None
    
    def build(self, user_input: str) -> Context:
        """Build context from user input following the pipeline."""
        context = Context(user_input=user_input)
        
        # Step 1: Conversation context
        context.conversation = self._get_conversation_context(user_input)
        
        # Step 2: Relevant memories
        context.memories = self._get_relevant_memories(user_input)
        
        # Step 3: Relevant lessons
        context.lessons = self._get_relevant_lessons(user_input)
        
        # Step 4: Relevant skills
        context.skills = self._get_relevant_skills(user_input)
        
        # Step 5: Security policies
        context.security_policies = self._get_security_policies(user_input)
        
        # Step 6: Final context
        context.final_context = self._build_final_context(context)
        
        return context
    
    def _get_conversation_context(self, user_input: str) -> List[Dict[str, Any]]:
        """Get conversation context."""
        return self._conversation_history[-10:]  # Last 10 messages
    
    def _get_relevant_memories(self, user_input: str) -> List[Dict[str, Any]]:
        """Get relevant memories from MemPalace via Searcher."""
        if not self._searcher or not _MEMPALACE_AVAILABLE:
            return []
        try:
            results = self._searcher.search(user_input, n_results=5)
            memories = []
            if results and results.get("drawers"):
                for doc, meta, dist in zip(
                    results["drawers"].get("documents", [[]])[0] if results["drawers"].get("documents") else [],
                    results["drawers"].get("metadatas", [[]])[0] if results["drawers"].get("metadatas") else [],
                    results["drawers"].get("distances", [[]])[0] if results["drawers"].get("distances") else []
                ):
                    memories.append({
                        "content": doc,
                        "metadata": meta,
                        "relevance": 1.0 - dist if dist else 0.0
                    })
            return memories
        except Exception:
            return []
    
    def _get_relevant_lessons(self, user_input: str) -> List[Dict[str, Any]]:
        """Get relevant lessons from MemPalace (Knowledge wing)."""
        if not self._searcher or not _MEMPALACE_AVAILABLE:
            return []
        try:
            results = self._searcher.search(user_input, wing="knowledge", n_results=3)
            lessons = []
            if results and results.get("drawers"):
                for doc, meta, dist in zip(
                    results["drawers"].get("documents", [[]])[0] if results["drawers"].get("documents") else [],
                    results["drawers"].get("metadatas", [[]])[0] if results["drawers"].get("metadatas") else [],
                    results["drawers"].get("distances", [[]])[0] if results["drawers"].get("distances") else []
                ):
                    lessons.append({
                        "content": doc,
                        "metadata": meta,
                        "type": "lesson"
                    })
            return lessons
        except Exception:
            return []
    
    def _get_relevant_skills(self, user_input: str) -> List[Dict[str, Any]]:
        """Get relevant skills from MemPalace (Technical wing)."""
        if not self._searcher or not _MEMPALACE_AVAILABLE:
            return []
        try:
            results = self._searcher.search(user_input, wing="technical", n_results=3)
            skills = []
            if results and results.get("drawers"):
                for doc, meta, dist in zip(
                    results["drawers"].get("documents", [[]])[0] if results["drawers"].get("documents") else [],
                    results["drawers"].get("metadatas", [[]])[0] if results["drawers"].get("metadatas") else [],
                    results["drawers"].get("distances", [[]])[0] if results["drawers"].get("distances") else []
                ):
                    skills.append({
                        "content": doc,
                        "metadata": meta,
                        "type": "skill"
                    })
            return skills
        except Exception:
            return []
    
    def _get_security_policies(self, user_input: str) -> List[Dict[str, Any]]:
        """Get security policies."""
        return [
            {"policy": "no_absolute_paths", "description": "Never use absolute host paths"},
            {"policy": "no_hardcoded_secrets", "description": "Never hardcode secrets"},
            {"policy": "validate_before_execute", "description": "Validate before executing"}
        ]
    
    def _build_final_context(self, context: Context) -> Dict[str, Any]:
        """Build final context from all components."""
        return {
            "user_input": context.user_input,
            "conversation_length": len(context.conversation),
            "memories_count": len(context.memories),
            "lessons_count": len(context.lessons),
            "skills_count": len(context.skills),
            "security_policies_count": len(context.security_policies),
            "timestamp": context.timestamp.isoformat()
        }
    
    def add_to_conversation(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        self._conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


# Global context builder instance
context_builder = ContextBuilder()
