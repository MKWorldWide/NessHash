import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ai.terra_voice_agent import TerraVoiceAgent


def test_voice_note_scheduling(tmp_path):
    calendar_path = tmp_path / "schedule.ics"
    agent = TerraVoiceAgent(calendar_path=calendar_path)
    agent.schedule_from_note("Convene solar council tomorrow at 09:00")
    assert "Convene solar council" in calendar_path.read_text()
