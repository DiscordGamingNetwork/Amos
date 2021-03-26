CREATE TABLE IF NOT EXISTS TriviaQuestions (
    id              SERIAL PRIMARY KEY,
    author_id       BIGINT NOT NULL REFERENCES Users (id),
    question        VARCHAR(512) NOT NULL,
    answers         VARCHAR(2048) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
