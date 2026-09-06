# Rideshare Passenger–Driver Language Relay

Status: Product Baseline

## Purpose

Any rideshare, taxi, chauffeur or transfer driver can open a temporary language channel.
The passenger scans a QR code and communicates in their preferred language; the driver
hears the translated message in the driver's selected language and can reply by voice.

This is a ride communication feature, not a tour, company assignment or official transport
partnership. It must work for an independent driver without requiring a tourism product.

## Ride flow

1. Driver explicitly starts a new ride relay and selects the driver output language.
2. The app creates a short-lived, single-session QR code; the raw token is not stored.
3. Passenger scans it, sees that this is a temporary communication channel, and chooses
   a language.
4. Passenger may speak or type. Driver receives voice output plus an optional large-text
   display when the vehicle is stationary.
5. Driver replies by voice. Passenger receives text and optional audio in their language.
6. Driver or passenger can end the relay; expiry also closes it automatically.

## Safety and truthfulness

- While the vehicle is moving, the driver interface is voice-first and must not require
  reading, typing or tapping through conversation screens.
- Emergency, address confirmation and safety-critical messages show the original text as
  well as the translation and invite confirmation; machine translation is not guaranteed.
- If STT, translation or TTS providers are not connected, the interface says
  “Not connected / Test mode” and does not claim live translation.
- The channel is not an emergency service and must not replace calling local emergency
  services when required.

## Privacy

- Ordinary ride conversation is ephemeral by default and does not enter the guide knowledge
  pack, contributor rewards, driver assessment or dispute-evidence store.
- QR tokens are short-lived and bound to one relay session; scanning does not reveal the
  driver's private phone number or the passenger's contact details.
- Recording is off by default. Enabling recording requires the separate company/driver and
  participant notice/consent workflow applicable to that ride and jurisdiction.
- Ending or expiring the relay revokes message access, subject only to a separately authorised
  retention or evidence hold.
