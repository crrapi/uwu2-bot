CREATE TABLE IF NOT EXISTS user_settings (
    user_id BIGINT PRIMARY KEY,
    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(512) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_adventures (
    user_id BIGINT PRIMARY KEY,
    end_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id BIGINT PRIMARY KEY NOT NULL,
    uwus_from_adventure BIGINT NOT NULL,
    foes_killed BIGINT NOT NULL,
    total_deaths BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS commands_used (
    commands_used BIGINT NOT NULL DEFAULT 1
);