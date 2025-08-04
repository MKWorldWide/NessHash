"""Calendar backend implementations for :class:`TerraVoiceAgent`.

The voice agent defaults to an ICS file-based backend for offline operation but can
optionally integrate with external calendar systems such as Google Calendar, CalDAV or
Microsoft Graph. Backends share an ``add_event`` interface to keep the agent decoupled
from storage specifics.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import time

from ics import Calendar, Event

# Third‑party client libraries are imported lazily inside each backend so deployments
# that only require local `.ics` support do not need them installed.


class CalendarBackend(ABC):
    """Abstract calendar backend interface."""

    @abstractmethod
    def add_event(self, event: Event) -> None:  # pragma: no cover - interface
        """Persist a newly created event."""

    @abstractmethod
    def serialize(self) -> str:  # pragma: no cover - interface
        """Return a serialized representation of the calendar."""


class ICSCalendarBackend(CalendarBackend):
    """Store events in a local `.ics` file for simple deployments."""

    def __init__(self, path: Path) -> None:
        self.path = path
        if path.exists():
            self.calendar = Calendar(path.read_text())
        else:
            self.calendar = Calendar()

    def add_event(self, event: Event) -> None:
        self.calendar.events.add(event)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(str(self.calendar))

    def serialize(self) -> str:
        return str(self.calendar)


class GoogleCalendarBackend(CalendarBackend):
    """Push events to a Google Calendar via OAuth2 service account credentials."""

    def __init__(self, credentials_file: Path, calendar_id: str) -> None:
        # Import lazily to keep optional dependency light for non-Google deployments
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        scopes = ["https://www.googleapis.com/auth/calendar"]
        self._creds = service_account.Credentials.from_service_account_file(
            str(credentials_file), scopes=scopes
        )
        self._builder = lambda: build(
            "calendar", "v3", credentials=self._creds, cache_discovery=False
        )
        self.service = self._builder()
        self.calendar_id = calendar_id

    def _insert_with_retry(self, body: dict) -> None:
        """Insert an event with token refresh and simple exponential backoff."""
        from googleapiclient.errors import HttpError
        from google.auth.transport.requests import Request

        for attempt in range(3):
            try:
                self.service.events().insert(
                    calendarId=self.calendar_id, body=body
                ).execute()
                return
            except HttpError as exc:
                if exc.resp.status in {401, 403}:
                    # Refresh token and rebuild service on auth errors
                    self._creds.refresh(Request())
                    self.service = self._builder()
                if attempt == 2:
                    raise
                time.sleep(0.1 * (2**attempt))

    def add_event(self, event: Event) -> None:
        body = {
            "summary": event.name,
            "start": {"dateTime": event.begin.isoformat()},
            "end": {"dateTime": (event.end or event.begin).isoformat()},
        }
        self._insert_with_retry(body)

    def serialize(self) -> str:
        # Events live externally; return a sentinel string for diagnostics.
        return "google-calendar"


class CalDAVBackend(CalendarBackend):
    """Store events on a CalDAV server."""

    def __init__(self, url: str, username: str, password: str) -> None:
        import caldav  # lazy import to keep optional

        client = caldav.DAVClient(url, username=username, password=password)
        self.calendar = client.principal().calendars()[0]

    def add_event(self, event: Event) -> None:
        self.calendar.add_event(str(event))

    def serialize(self) -> str:
        return "caldav"


class MicrosoftGraphBackend(CalendarBackend):
    """Push events to Microsoft 365 calendars via Microsoft Graph."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        calendar_id: str = "primary",
    ) -> None:
        import msal  # lazy import

        self._calendar_id = calendar_id
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        self._app = msal.ConfidentialClientApplication(
            client_id, authority=authority, client_credential=client_secret
        )
        self._scope = ["https://graph.microsoft.com/.default"]

    def _token(self) -> str:
        result = self._app.acquire_token_silent(self._scope, account=None)
        if not result:
            result = self._app.acquire_token_for_client(scopes=self._scope)
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description", "Token acquisition failed"))
        return result["access_token"]

    def add_event(self, event: Event) -> None:
        import requests  # lazy import for optional dependency

        token = self._token()
        url = (
            f"https://graph.microsoft.com/v1.0/me/calendars/{self._calendar_id}/events"
        )
        body = {
            "subject": event.name,
            "start": {"dateTime": event.begin.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": (event.end or event.begin).isoformat(), "timeZone": "UTC"},
        }
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        requests.post(url, json=body, headers=headers, timeout=10)

    def serialize(self) -> str:
        return "microsoft-graph"

