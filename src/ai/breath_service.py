"""Breath sensor ingestion and climate actuation service.

Acts as the bridge between raw sensor packets and the `ClimateBrain` AI
engine. Normalizes input, triggers predictions, and dispatches the resulting
commands to actuators.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure local imports work when running this file directly
sys.path.append(str(Path(__file__).resolve().parent))

from actuator_dispatcher import ActuatorDispatcher
from divine_climate_brain import ClimateBrain, SensorPacket

logger = logging.getLogger(__name__)


class BreathService:
    """Service orchestration for breath-driven terraforming."""

    def __init__(self) -> None:
        self.brain = ClimateBrain()
        self.dispatcher = ActuatorDispatcher()

    def receive_breath(self, raw: Dict[str, Any]) -> None:
        """Normalize and ingest breath sensor data.

        Args:
            raw: Unprocessed sensor metrics from wearables or edge devices.
        """
        # TODO: Apply validation and normalization of raw packet values
        packet = SensorPacket(data=raw)
        logger.info("Received breath packet: %s", packet)
        self.brain.ingest_sensor_data(packet)

    def process(self) -> None:
        """Run prediction and dispatch actuator directives."""
        directives = self.brain.predict()
        self.dispatcher.dispatch(directives)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = BreathService()
    # Example payload representing breath-derived metrics
    service.receive_breath({"temp": 21.5, "humidity": 0.44})
    service.process()
