# RUNTIME CONTRACT NO.001

LiveContext:
- session_id
- time
- motion_state
- gps
- route_id
- previous_place_id
- next_expected_places
- vision
- guide_voice_hint
- visitor_question
- active_timeline

RecognitionResult:
- candidates[]
- selected_place_id
- confidence
- evidence
- needs_confirmation

NarrationRequest:
- place_id
- timeline_id
- experience_pack_ids
- guide_style
- audience
- language
- duration_seconds
- output_mode

Driving rule:
motion_state=moving 时，非关键内容不得要求屏幕确认。
