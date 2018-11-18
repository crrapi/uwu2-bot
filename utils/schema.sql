CREATE TABLE IF NOT EXISTS user_settings (
    user_id BIGINT PRIMARY KEY,
    time_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(512) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_timers (
    user_id BIGINT NOT NULL,
    end_time TIMESTAMP NOT NULL,
    timer_type INT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id BIGINT PRIMARY KEY NOT NULL,
    uwus BIGINT NOT NULL,
    foes_killed BIGINT NOT NULL,
    total_deaths BIGINT NOT NULL,
    current_level BIGINT NOT NULL DEFAULT 0,
    current_xp BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS commands_used (
    commands_used BIGINT NOT NULL DEFAULT 1
);