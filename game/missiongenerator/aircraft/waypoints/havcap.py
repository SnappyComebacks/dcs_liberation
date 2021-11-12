import logging
from dcs.mapping import Point
from dcs.point import MovingPoint
from dcs.task import CAPTaskAction, Follow
from game.missiongenerator.aircraft.waypoints.pydcswaypointbuilder import (
    PydcsWaypointBuilder,
)
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
            waypoint.add_task(CAPTaskAction())

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
