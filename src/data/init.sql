CREATE TABLE IF NOT EXISTS Users (
    id              BIGINT NOT NULL PRIMARY KEY,
    xp              BIGINT NOT NULL DEFAULT 0,
    perms           BIGINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Topics (
    id              SERIAL PRIMARY KEY,
    author_id       BIGINT NOT NULL REFERENCES Users (id),
    topic           VARCHAR(512) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
