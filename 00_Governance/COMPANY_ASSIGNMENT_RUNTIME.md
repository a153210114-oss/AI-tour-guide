# COMPANY ASSIGNMENT RUNTIME

Status: Governance Baseline

## Principle

For company-operated tours, an accepted assignment is the runtime source of truth.
The system must not infer the company's product from GPS alone.

`Company -> Product -> Product Version -> Assignment -> Tour Session`

The assignment tells the runtime which driver or guide is operating which product,
route, content versions, languages and playback policy. GPS and recognition then determine
where that assigned tour is currently operating.

## Start flow

1. Company publishes an immutable Product Version.
2. Operations creates a dated assignment for a driver/guide and vehicle.
3. The assignee accepts the assignment.
4. At tour start, the assignee selects the assignment when more than one is eligible.
5. The assigned driver explicitly authorizes location access for this assignment.
6. Runtime creates a Tour Session locked to that Product Version.
7. The offline bundle loads route, stops, content references, language channels and
   autoplay rules.
8. GPS, direction, speed, sequence and recognition advance the session.

Company dispatch does not grant location permission. Before authorization, the driver can
view and accept an assignment, but location recognition and autoplay remain unavailable.
Permission state must distinguish not requested, granted, denied, device restricted and
revoked. Consent is specific to the assigned driver and assignment, can be revoked, and
must not be reused after reassignment.

Editing a product does not mutate an active Tour Session. A new Product Version applies
to a future assignment unless operations explicitly migrates an unstarted assignment.

## Required exceptions

- Driver/guide replacement creates an auditable reassignment event.
- Vehicle replacement does not change the locked product or content.
- Route detours create deviation events and must not silently rewrite the product route.
- Temporary stops are session events, not permanent product changes.
- Offline start is supported after the assignment bundle has been downloaded.
- Emergency stop and mute always override autoplay.
- Revoking location permission stops location collection, recognition and autoplay.
