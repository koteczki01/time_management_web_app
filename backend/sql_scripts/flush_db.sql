-- THIS SCRIPT WILL RESET THE DATABASE TO A CLEAN STATE

-- DELETE ALL DATA
DELETE FROM db_event_participants;
DELETE FROM db_user_friendship;
DELETE FROM db_event_category;
DELETE FROM db_event;
DELETE FROM db_category;
DELETE FROM db_user;

-- RESET ALL SEQUENCES
ALTER SEQUENCE db_user_user_id_seq RESTART WITH 1;
ALTER SEQUENCE db_category_category_id_seq RESTART WITH 1;
ALTER SEQUENCE db_event_event_id_seq RESTART WITH 1;
ALTER SEQUENCE db_user_friendship_friendship_id_seq RESTART WITH 1;
