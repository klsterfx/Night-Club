-- Drop existing tables (if they exist)
DROP TABLE IF EXISTS clubs CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS bouncers CASCADE;
DROP TABLE IF EXISTS managers CASCADE;
DROP TABLE IF EXISTS waiting_list CASCADE;
DROP TABLE IF EXISTS reservations CASCADE;
DROP TABLE IF EXISTS entered CASCADE;

-- Create the 'clubs' table to store information about clubs
CREATE TABLE clubs (
  name VARCHAR(32) NOT NULL UNIQUE, -- Name of the club (unique)
  capacity INT NOT NULL, -- Maximum capacity of the club
  city VARCHAR(50), -- City where the club is located
  opening_time timestamp, -- Opening time of the club
  closing_time timestamp, -- Closing time of the club
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the record was last modified
  PRIMARY KEY(name) -- Primary key for the 'clubs' table
);

-- Create the 'users' table to store information about users
CREATE TABLE users (
  name VARCHAR(32) NOT NULL UNIQUE, -- User's name (unique)
  password VARCHAR(128) NOT NULL, -- User's password (hashed)
  age INT, -- User's age
  email VARCHAR(50), -- User's email
  city VARCHAR(50), -- User's city
  session_id INT, -- User's session ID (if applicable)
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the user record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the user record was last modified
  PRIMARY KEY(name) -- Primary key for the 'users' table
);

-- Create the 'bouncers' table to link users with clubs
CREATE TABLE bouncers (
  user_name VARCHAR(32), -- User's name
  club_name VARCHAR(32), -- Club's name
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the bouncer record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the bouncer record was last modified
  PRIMARY KEY(user_name), -- Primary key for the 'bouncers' table
  CONSTRAINT fk_club FOREIGN KEY(club_name) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(user_name) REFERENCES users(name) ON UPDATE CASCADE -- Foreign key reference to 'users' table
);

-- Create the 'managers' table to link users with clubs (similar to 'bouncers')
CREATE TABLE managers (
  user_name VARCHAR(32), -- User's name
  club_name VARCHAR(32), -- Club's name
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was last modified
  PRIMARY KEY(user_name), -- Primary key for the 'managers' table
  CONSTRAINT fk_club FOREIGN KEY(club_name) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(user_name) REFERENCES users(name) ON UPDATE CASCADE -- Foreign key reference to 'users' table
);

-- Create the 'waiting_list' table to store waiting list information
CREATE TABLE waiting_list (
  id SERIAL, -- Unique identifier for waiting list entries
  user_name VARCHAR(32), -- User's name
  club_name VARCHAR(32), -- Club's name
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the waiting list record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the waiting list record was last modified
  PRIMARY KEY(id), -- Primary key for the 'waiting_list' table
  CONSTRAINT fk_club FOREIGN KEY(club_name) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(user_name) REFERENCES users(name) ON UPDATE CASCADE -- Foreign key reference to 'users' table
);

-- Create the 'reservations' table to store reservation information
CREATE TABLE reservations (
  id SERIAL, -- Unique identifier for reservations
  user_name VARCHAR(32), -- User's name
  club_name VARCHAR(32), -- Club's name
  reservation_start_time timestamp, -- Start time of the reservation
  reservation_end_time timestamp, -- End time of the reservation
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the reservation record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the reservation record was last modified
  PRIMARY KEY(id), -- Primary key for the 'reservations' table
  CONSTRAINT fk_club FOREIGN KEY(club_name) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(user_name) REFERENCES users(name) ON UPDATE CASCADE -- Foreign key reference to 'users' table
);

-- Create the 'entered' table to store information about users entering clubs
CREATE TABLE entered (
  id SERIAL, -- Unique identifier for entry records
  user_name VARCHAR(32), -- User's name
  club_name VARCHAR(32), -- Club's name
  enter_time timestamp, -- Time when the user entered the club
  amount_spent float, -- Amount spent by the user during the visit
  left_time timestamp, -- Time when the user left the club
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the entry record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the entry record was last modified
  PRIMARY KEY(id), -- Primary key for the 'entered' table
  CONSTRAINT fk_club FOREIGN KEY(club_name) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(user_name) REFERENCES users(name) ON UPDATE CASCADE -- Foreign key reference to 'users' table
);

-- Define a trigger function to update 'last_modified_at' timestamp
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.last_modified_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers to automatically update 'last_modified_at' when records are updated
CREATE TRIGGER set_timestamp_clubs BEFORE UPDATE ON clubs FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_users BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_bouncers BEFORE UPDATE ON bouncers FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_managers BEFORE UPDATE ON managers FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_reservations BEFORE UPDATE ON reservations FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_entered BEFORE UPDATE ON entered FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER set_timestamp_waiting_list BEFORE UPDATE ON waiting_list FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
