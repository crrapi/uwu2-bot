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
    user_id BIGINT PRIMARY KEY NOT NULL REFERENCES user_settings(user_id),
    uwus BIGINT NOT NULL,
    foes_killed BIGINT NOT NULL,
    total_deaths BIGINT NOT NULL,
    current_level BIGINT NOT NULL DEFAULT 0,
    current_xp BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS marriages (
    user1_id BIGINT PRIMARY KEY NOT NULL REFERENCES user_settings(user_id),
    user2_id BIGINT NOT NULL,
    patron_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS commands_used (
    commands_used BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS p_user_timer (
    user_id BIGINT PRIMARY KEY NOT NULL,
    next_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS p_users (
    user_id BIGINT PRIMARY KEY NOT NULL,
    patron_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_badges (
    user_id BIGINT PRIMARY KEY NOT NULL REFERENCES user_settings(user_id),
    badges TEXT[] NOT NULL
);


--ALTER TABLE marriages ADD CONSTRAINT user_marriages_user_id_fkey FOREIGN KEY (user1_id) REFERENCES user_settings (user_id) ON DELETE CASCADE;")
--ALTER TABLE user_badges ADD CONSTRAINT user_badges_user_id_fkey FOREIGN KEY (user_id) REFERENCES user_settings (user_id) ON DELETE CASCADE;")