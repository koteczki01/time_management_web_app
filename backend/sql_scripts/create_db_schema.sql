-- CREATE DB
CREATE DATABASE quanta;

-- CREATE TYPES
CREATE TYPE privacy_level AS ENUM ('public', 'private');
CREATE TYPE status AS ENUM ('pending', 'accepted');
CREATE TYPE recurrence_rule AS ENUM ('daily', 'weekly', 'monthly', 'yearly');
CREATE TYPE event_role AS ENUM ('host', 'member');


-- DONE
CREATE TABLE db_category(
    category_id SERIAL PRIMARY KEY,
    category_name varchar(45) UNIQUE,
    category_description varchar(255) NULL
);


-- DONE
CREATE TABLE db_user(
    user_id SERIAL PRIMARY KEY,
    username varchar(45) NOT NULL,
    email varchar(60) NOT NULL,
    password_hash varchar(60) NOT NULL,
    birthday date NOT NULL,
    created_at timestamp NOT NULL,
    last_login timestamp NOT NULL,
    update_date timestamp NOT NULL,
    is_active boolean NOT NULL
);
ALTER TABLE db_user ADD UNIQUE(username, email);

-- DONE
CREATE TABLE db_event(
    event_id SERIAL PRIMARY KEY,
    created_by int NOT NULL REFERENCES db_user(user_id),
    event_name varchar(60) NOT NULL,
    event_description varchar(255) NULL,
    event_date_start timestamp not NULL,
    event_date_end timestamp NOT NULL,
    event_location varchar(255) NULL,
    privacy privacy_level NOT NULL,
	recurrence recurrence_rule NOT NULL,
	next_event_date timestamp NULL
);


-- DONE
CREATE TABLE db_event_category(
    event_id int NOT NULL,
    category_id int NOT NULL,
    PRIMARY KEY(event_id, category_id),

    CONSTRAINT fk_event_id FOREIGN KEY(event_id) REFERENCES db_event(event_id),
    CONSTRAINT fk_category_id FOREIGN KEY(category_id) REFERENCES db_category(category_id)
);


-- DONE
CREATE TABLE db_user_friendship(
    friendship_id SERIAL PRIMARY KEY,
    user1_id int NOT NULL,
    user2_id int NOT NULL,
    friendship_status status NOT NULL,

    CONSTRAINT fk_user1_id FOREIGN KEY(user1_id) REFERENCES db_user(user_id),
    CONSTRAINT fk_user2_id FOREIGN KEY(user2_id) REFERENCES db_user(user_id)
);

-- DONE
CREATE TABLE db_event_participants (
    event_id INT,
    user_id INT,
    participant_status status NOT NULL,
    participant_role event_role NOT NULL,
    response_time timestamp NOT NULL,

	PRIMARY KEY (event_id, user_id),
    CONSTRAINT fk_event_for_participants FOREIGN KEY (event_id) REFERENCES db_event(event_id),
    CONSTRAINT fk_participants_for_events FOREIGN KEY (user_id) REFERENCES db_user(user_id)
);