import logging
import math
from typing import Type
from dcs.mapping import Point
from dcs.point import MovingPoint
from dcs.task import EngageTargets, Follow, Targets
from game.missiongenerator.aircraft.waypoints.pydcswaypointbuilder import (
    PydcsWaypointBuilder,
)
from game.utils import Distance
from gen.flights.flightplan import HavCapFlightPlan


class HavcapPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if not isinstance(self.flight.flight_plan, HavCapFlightPlan):
            logging.error(
                "Incorrect flight type for mission: %s",
                self.flight.flight_type,
            )
            return super().add_tasks(waypoint)
        else:

            engage_range = Distance.from_nautical_miles(40)
            planes = Targets.All.Air.Planes
            engage_targets = [
                Type[planes.Fighters],
                Type[planes.MultiroleFighters],
                Type[Targets.All.Air.Helicopters],
            ]
            search_and_engage = EngageTargets(
                max_distance=math.floor(engage_range.nautical_miles),
                targets=engage_targets,
            )
            waypoint.add_task(search_and_engage)

            flight_plan = self.flight.flight_plan

            group_id = flight_plan.escorted_group_id
            altitude_difference = flight_plan.altitude_offset.feet
            position = Point(flight_plan.x_offset.feet, flight_plan.y_offset.feet)
            last_wpt = flight_plan.last_escorted_waypoint

            waypoint.add_task(
                Follow(
                    groupid=group_id,
                    position=position,
                    altitude_difference=altitude_difference,
                    last_wpt=last_wpt,
                )
            )

            return super().add_tasks(waypoint)
