CREATE TABLE companies (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  logo_object_key TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE guides (
  id TEXT PRIMARY KEY,
  company_id TEXT REFERENCES companies(id),
  guide_number TEXT NOT NULL,
  name TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT 'company',
  created_at TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_guides_company_number ON guides(company_id, guide_number);

CREATE TABLE tour_sessions (
  id TEXT PRIMARY KEY,
  company_id TEXT REFERENCES companies(id),
  guide_id TEXT NOT NULL REFERENCES guides(id),
  route_name TEXT NOT NULL,
  product_name TEXT NOT NULL,
  service_date TEXT NOT NULL,
  vehicle TEXT,
  status TEXT NOT NULL DEFAULT 'scheduled',
  join_token_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_tour_sessions_guide_date ON tour_sessions(guide_id, service_date);
CREATE INDEX idx_tour_sessions_company_date ON tour_sessions(company_id, service_date);

CREATE TABLE visitors (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES tour_sessions(id),
  locale TEXT NOT NULL,
  joined_at TEXT NOT NULL
);

CREATE INDEX idx_visitors_session ON visitors(session_id);

CREATE TABLE questions (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES tour_sessions(id),
  visitor_id TEXT NOT NULL REFERENCES visitors(id),
  locale TEXT NOT NULL,
  question_text TEXT NOT NULL,
  answer_text TEXT,
  status TEXT NOT NULL DEFAULT 'waiting',
  created_at TEXT NOT NULL,
  answered_at TEXT
);

CREATE INDEX idx_questions_session_created ON questions(session_id, created_at);

CREATE TABLE ratings (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES tour_sessions(id),
  visitor_id TEXT NOT NULL REFERENCES visitors(id),
  score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
  tags_json TEXT NOT NULL DEFAULT '[]',
  comment TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);

CREATE INDEX idx_ratings_session_created ON ratings(session_id, created_at);

CREATE TABLE audio_segments (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES tour_sessions(id),
  guide_id TEXT NOT NULL REFERENCES guides(id),
  object_key TEXT NOT NULL UNIQUE,
  started_at TEXT NOT NULL,
  ended_at TEXT NOT NULL,
  latitude REAL,
  longitude REAL,
  place_name TEXT,
  transcript_text TEXT,
  source_language TEXT,
  consent_basis TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_audio_segments_session_started ON audio_segments(session_id, started_at);
CREATE INDEX idx_audio_segments_place ON audio_segments(place_name);

CREATE TABLE content_packs (
  id TEXT PRIMARY KEY,
  owner_company_id TEXT REFERENCES companies(id),
  owner_guide_id TEXT REFERENCES guides(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TEXT NOT NULL
);

CREATE TABLE content_pack_items (
  id TEXT PRIMARY KEY,
  pack_id TEXT NOT NULL REFERENCES content_packs(id),
  place_name TEXT NOT NULL,
  script_text TEXT,
  audio_segment_id TEXT REFERENCES audio_segments(id),
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_content_pack_items_pack ON content_pack_items(pack_id, sort_order);

CREATE TABLE content_pack_grants (
  id TEXT PRIMARY KEY,
  pack_id TEXT NOT NULL REFERENCES content_packs(id),
  grantee_company_id TEXT REFERENCES companies(id),
  grantee_guide_id TEXT REFERENCES guides(id),
  permission TEXT NOT NULL DEFAULT 'use',
  granted_at TEXT NOT NULL,
  revoked_at TEXT
);

CREATE INDEX idx_content_pack_grants_pack ON content_pack_grants(pack_id);
