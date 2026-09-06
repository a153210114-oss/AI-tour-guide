from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AutoplayRule:
    rule_id: str
    route_id: str
    place_id: str
    audio_asset_id: str
    geofence_radius_m: int
    route_direction: str | None
    minimum_speed_kph: float | None
    maximum_speed_kph: float | None
    guide_preview_seconds: int
    once_per_session: bool = True


@dataclass(frozen=True)
class PlaybackContext:
    route_id: str
    route_direction: str | None
    distance_to_place_m: float
    expected_place_ids: tuple[str, ...]
    current_speed_kph: float
    emergency_muted: bool
    already_played_rule_ids: frozenset[str]


def may_autoplay(rule: AutoplayRule, context: PlaybackContext) -> bool:
    if context.emergency_muted:
        return False
    if rule.route_id != context.route_id:
        return False
    if rule.route_direction is not None and rule.route_direction != context.route_direction:
        return False
    if rule.place_id not in context.expected_place_ids:
        return False
    if context.distance_to_place_m > rule.geofence_radius_m:
        return False
    if rule.once_per_session and rule.rule_id in context.already_played_rule_ids:
        return False
    if rule.minimum_speed_kph is not None and context.current_speed_kph < rule.minimum_speed_kph:
        return False
    if rule.maximum_speed_kph is not None and context.current_speed_kph > rule.maximum_speed_kph:
        return False
    return True
