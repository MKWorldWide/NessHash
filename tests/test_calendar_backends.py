import sys
from datetime import datetime
from pathlib import Path

from ics import Event

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ai import calendar_backends as cb


def test_google_backend_refresh(monkeypatch, tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text("{}")

    class DummyCreds:
        def __init__(self):
            self.refresh_count = 0

        def refresh(self, request):
            self.refresh_count += 1

    def fake_from_file(path, scopes):
        return DummyCreds()

    class DummyService:
        def __init__(self, fail_first: bool):
            self.fail_first = fail_first
            self.calls = 0

        def events(self):
            return self

        def insert(self, calendarId, body):
            return self

        def execute(self):
            from googleapiclient.errors import HttpError
            from httplib2 import Response

            self.calls += 1
            if self.fail_first and self.calls == 1:
                raise HttpError(Response({'status': 401}), b'', uri='')
            return {}

    services = []

    def fake_build(*args, **kwargs):
        svc = DummyService(fail_first=not services)
        services.append(svc)
        return svc

    import google.oauth2.service_account as sa
    import googleapiclient.discovery as discovery
    monkeypatch.setattr(sa.Credentials, "from_service_account_file", fake_from_file)
    monkeypatch.setattr(discovery, "build", fake_build)

    backend = cb.GoogleCalendarBackend(creds_file, "cal")
    backend.add_event(Event(name="Test", begin=datetime.utcnow()))

    assert services[0].calls == 1
    assert services[1].calls == 1
    assert backend._creds.refresh_count == 1
