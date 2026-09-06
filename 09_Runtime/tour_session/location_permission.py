from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum


class LocationPermissionStatus(str, Enum):
    NOT_REQUESTED = "not_requested"
    GRANTED = "granted"
    DENIED = "denied"
    RESTRICTED = "restricted"
    REVOKED = "revoked"


@dataclass(frozen=True)
class DriverLocationAuthorization:
    driver_id: str
    assignment_id: str
    status: LocationPermissionStatus = LocationPermissionStatus.NOT_REQUESTED
    granted_at: datetime | None = None
    revoked_at: datetime | None = None

    def grant(self, actor_id: str, granted_at: datetime) -> "DriverLocationAuthorization":
        if actor_id != self.driver_id:
            raise PermissionError("only the assigned driver can authorize location")
        return replace(
            self,
            status=LocationPermissionStatus.GRANTED,
            granted_at=granted_at,
            revoked_at=None,
        )

    def deny(self, actor_id: str) -> "DriverLocationAuthorization":
        if actor_id != self.driver_id:
            raise PermissionError("only the assigned driver can deny location")
        return replace(self, status=LocationPermissionStatus.DENIED, granted_at=None)

    def revoke(self, actor_id: str, revoked_at: datetime) -> "DriverLocationAuthorization":
        if actor_id != self.driver_id:
            raise PermissionError("only the assigned driver can revoke location")
        return replace(
            self,
            status=LocationPermissionStatus.REVOKED,
            granted_at=None,
            revoked_at=revoked_at,
        )

    def authorizes(self, driver_id: str, assignment_id: str) -> bool:
        return (
            self.status is LocationPermissionStatus.GRANTED
            and self.driver_id == driver_id
            and self.assignment_id == assignment_id
            and self.granted_at is not None
        )
