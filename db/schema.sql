-- schema.sql — storage for the review bar (comments + inline text edits).
--
-- One row per comment and per edit, rather than one JSON blob per prototype.
-- That is deliberate: every write touches a single row, so two reviewers posting
-- at the same moment can no longer overwrite each other (the blob store had to
-- read-modify-write the whole document, which lost updates under concurrency).
--
-- Apply once against the Neon database:
--   psql "$DATABASE_URL" -f db/schema.sql
-- Re-running is safe.

create table if not exists comments (
  id          text primary key,              -- client-generated, e.g. 'cm1a2b3c'
  prototype   text        not null,          -- '/workflow-view/'
  n           integer     not null,          -- display number, 1..n per prototype
  path        text,                          -- element address, 'root/0.2.1'
  el          text,                          -- human label, 'button.btn "Save"'
  html        text,
  screen_id   text,
  screen      text,
  url         text,
  rect        jsonb,
  body        text        not null default '',
  author      text,
  resolved    boolean     not null default false,
  resolution  text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  deleted_at  timestamptz                    -- soft delete: nothing is ever truly lost
);

-- Display numbers are unique per prototype among live comments.
create unique index if not exists comments_prototype_n
  on comments (prototype, n) where deleted_at is null;

-- The hot path: fetch one prototype's live comments.
create index if not exists comments_prototype_live
  on comments (prototype) where deleted_at is null;

create table if not exists edits (
  prototype   text        not null,
  key         text        not null,          -- '<element path>#<text node index>'
  orig        text        not null,          -- original copy, so the edit can be undone
  text        text        not null,          -- replacement copy
  screen      text,
  author      text,
  updated_at  timestamptz not null default now(),
  primary key (prototype, key)
);

-- Per-prototype comment numbering. Incremented atomically so two reviewers
-- posting at the same instant always get distinct numbers; computing
-- max(n)+1 instead would let both read the same stale maximum.
-- Numbers are never reused, so deleting a comment doesn't renumber the rest.
create table if not exists counters (
  prototype text primary key,
  last_n    integer not null default 0
);
