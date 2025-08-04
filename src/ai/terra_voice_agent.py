"""NessHash voice agent expanded into a scheduling engine."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from dateparser.search import search_dates
from ics import Event

from .calendar_backends import CalendarBackend, ICSCalendarBackend


class TerraVoiceAgent:
    """Parses voice notes into calendar events and persists them via a backend."""

    def __init__(
        self,
        backend: Optional[CalendarBackend] = None,
        calendar_path: Optional[Path] = None,
    ) -> None:
        """Initialize the agent with a calendar backend.

        Parameters
        ----------
        backend:
            Custom backend; if omitted an ``ICSCalendarBackend`` is created using
            ``calendar_path``.
        calendar_path:
            Location of the `.ics` file when using the default backend.
        """

        if backend is not None:
            self.backend = backend
        else:
            path = calendar_path or Path("data/schedule.ics")
            self.backend = ICSCalendarBackend(path)

    def schedule_from_note(self, note: str) -> Event:
        """Parse a natural-language note and append it to the calendar."""
        result = search_dates(note, settings={"PREFER_DATES_FROM": "future"})
        if not result:
            raise ValueError("Unable to parse date from note")
        phrase, dt = result[0]
        description = note.replace(phrase, "").strip() or "Voice note"
        event = Event(name=description, begin=dt)
        self.backend.add_event(event)
        return event

    def inhale(self, data: str) -> Event:
        """Alias for schedule_from_note to fit agent metaphor."""
        return self.schedule_from_note(data)

    def exhale(self) -> str:
        """Return the serialized calendar representation from the backend."""
        return self.backend.serialize()
