from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from importlib import import_module

agency = import_module("13_Commercial.agency.assignment")
location_permission = import_module("09_Runtime.tour_session.location_permission")
AssignmentStatus = agency.AssignmentStatus
CompanyAssignment = agency.CompanyAssignment
CompanyProductVersion = agency.CompanyProductVersion
LanguageChannels = agency.LanguageChannels
DriverLocationAuthorization = location_permission.DriverLocationAuthorization


@dataclass(frozen=True)
class CompanyTourSession:
    session_id: str
    assignment_id: str
    company_id: str
    product_id: str
    locked_product_version: str
    route_id: str
    driver_id: str
    guide_id: str | None
    vehicle_id: str | None
    started_at: datetime
    planned_stop_ids: tuple[str, ...]
    content_pack_versions: tuple[str, ...]
    autoplay_policy_id: str | None
    languages: LanguageChannels
    offline_bundle_id: str
    location_authorized_by_driver_at: datetime


def start_company_tour(
    *,
    session_id: str,
    assignment: CompanyAssignment,
    product: CompanyProductVersion,
    actor_id: str,
    started_at: datetime,
    offline_bundle_id: str,
    location_authorization: DriverLocationAuthorization,
) -> CompanyTourSession:
    if assignment.status is not AssignmentStatus.ACCEPTED:
        raise ValueError("assignment must be accepted before tour start")
    if actor_id not in {assignment.driver_id, assignment.guide_id}:
        raise PermissionError("actor is not assigned to this tour")
    identity = (
        assignment.company_id,
        assignment.product_id,
        assignment.product_version,
        assignment.route_id,
    )
    expected = (product.company_id, product.product_id, product.version, product.route_id)
    if identity != expected:
        raise ValueError("assignment does not match the published product version")
    if not offline_bundle_id:
        raise ValueError("a downloaded offline bundle is required")
    if not location_authorization.authorizes(
        assignment.driver_id, assignment.assignment_id
    ):
        raise PermissionError("assigned driver location authorization is required")
    return CompanyTourSession(
        session_id=session_id,
        assignment_id=assignment.assignment_id,
        company_id=assignment.company_id,
        product_id=assignment.product_id,
        locked_product_version=product.version,
        route_id=product.route_id,
        driver_id=assignment.driver_id,
        guide_id=assignment.guide_id,
        vehicle_id=assignment.vehicle_id,
        started_at=started_at,
        planned_stop_ids=product.planned_stop_ids,
        content_pack_versions=product.content_pack_versions,
        autoplay_policy_id=product.autoplay_policy_id,
        languages=product.languages,
        offline_bundle_id=offline_bundle_id,
        location_authorized_by_driver_at=location_authorization.granted_at,
    )
