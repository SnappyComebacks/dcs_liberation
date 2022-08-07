from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import (
    GarrisonGroundObject,
    VehicleGroupGroundObject,
)
from game.ato.flighttype import FlightType


@dataclass
class PlanBai(PackagePlanningTask[VehicleGroupGroundObject | GarrisonGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if isinstance(
            self.target, VehicleGroupGroundObject
        ) and not state.has_battle_position(self.target):
            return False
        elif isinstance(self.target, GarrisonGroundObject) and not state.has_garrisons(
            self.target
        ):
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_bai_position(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.BAI, 2)
        self.propose_common_escorts()
