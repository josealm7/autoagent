from __future__ import annotations
from datetime import datetime, timedelta
from collections import defaultdict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

MAX_HISTORY_TURNS = 8
SESSION_TTL_MINUTES = 60


class SessionStore:
    def __init__(self):
        self._sessions: dict[str, list[BaseMessage]] = defaultdict(list)
        self._last_active: dict[str, datetime] = {}

    def get_history(self, session_id: str) -> list[BaseMessage]:
        self._cleanup_expired()
        return self._sessions.get(session_id, [])

    def add_turn(self, session_id: str, user_msg: str, ai_msg: str) -> None:
        history = self._sessions[session_id]
        history.append(HumanMessage(content=user_msg))
        history.append(AIMessage(content=ai_msg))
        if len(history) > MAX_HISTORY_TURNS * 2:
            self._sessions[session_id] = history[-(MAX_HISTORY_TURNS * 2):]
        self._last_active[session_id] = datetime.utcnow()

    def clear_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        self._last_active.pop(session_id, None)

    def _cleanup_expired(self) -> None:
        cutoff = datetime.utcnow() - timedelta(minutes=SESSION_TTL_MINUTES)
        expired = [sid for sid, t in self._last_active.items() if t < cutoff]
        for sid in expired:
            self._sessions.pop(sid, None)
            self._last_active.pop(sid, None)

    @property
    def active_sessions(self) -> int:
        return len(self._sessions)


session_store = SessionStore()
