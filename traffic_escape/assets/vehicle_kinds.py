"""Vehicle categories available on the highway."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleKind:
    name: str
    width: int
    height: int
    speed_range: tuple[float, float]


CAR = VehicleKind("car", 64, 108, (2.6, 5.4))
PICKUP = VehicleKind("pickup", 68, 120, (2.2, 4.4))
TRUCK = VehicleKind("truck", 74, 150, (1.2, 2.8))
BUS = VehicleKind("bus", 70, 160, (1.0, 2.6))

# Cars appear more often than heavy vehicles.
TRAFFIC_KINDS = (CAR, CAR, CAR, PICKUP, TRUCK, BUS)
PLAYER_KIND = CAR
