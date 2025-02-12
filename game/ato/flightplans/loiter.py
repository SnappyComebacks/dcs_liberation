from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING, TypeGuard, TypeVar

from game.flightplan.waypointactions.hold import Hold
from game.typeguard import self_type_guard
from game.utils import Speed
from .flightplan import FlightPlan
from .standard import StandardFlightPlan, StandardLayout

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class LoiterLayout(StandardLayout, ABC):
    hold: FlightWaypoint


LayoutT = TypeVar("LayoutT", bound=LoiterLayout)


class LoiterFlightPlan(StandardFlightPlan[LayoutT], ABC):
    @property
    def hold_duration(self) -> timedelta:
        return timedelta(minutes=5)

    @property
    @abstractmethod
    def push_time(self) -> datetime: ...

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.hold:
            return self.push_time
        return None

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().total_time_between_waypoints(a, b)
        if a != self.layout.hold:
            return travel_time
        return travel_time + self.hold_duration

    @self_type_guard
    def is_loiter(
        self, flight_plan: FlightPlan[Any]
    ) -> TypeGuard[LoiterFlightPlan[Any]]:
        return True

    def provide_push_time(self) -> datetime:
        return self.push_time

    def add_waypoint_actions(self) -> None:
        hold = self.layout.hold
        speed = self.flight.unit_type.patrol_speed
        if speed is None:
            speed = Speed.from_mach(0.6, hold.alt)
        hold.add_action(Hold(self.provide_push_time, hold.alt, speed))
