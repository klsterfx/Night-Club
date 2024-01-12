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
  city VARCHAR(50), -- City where the club is located
  music VARCHAR(32),
  capacity INT NOT NULL, -- Maximum capacity of the club
  yellow_threshold INT NOT NULL, 
  current_count INT default 0,
  increment boolean default false, 
  decrement boolean default false,
  PRIMARY KEY(name) -- Primary key for the 'clubs' table
);


-- Create the 'users' table to store information about users
CREATE TABLE users (
  name VARCHAR(32) NOT NULL, -- User's name (unique)
  password VARCHAR(128) NOT NULL, -- User's password (hashed)
  age INT, -- User's age
  email VARCHAR(50) NOT NULL UNIQUE, -- User's email
  city VARCHAR(50), -- User's city
  role VARCHAR(50) default 'user',
  session_id INT, -- User's session ID (if applicable)
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the user record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the user record was last modified
  PRIMARY KEY(email) -- Primary key for the 'users' table
);


-- Create the 'entered' table to store information about users entering clubs
CREATE TABLE entered (
  id SERIAL, -- Unique identifier for entry records
  email VARCHAR(32), -- User's name
  club VARCHAR(32), -- Club's name
  enter_time timestamp, -- Time when the user entered the club
  amount_spent float, -- Amount spent by the user during the visit
  left_time timestamp , -- Time when the user left the club
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the entry record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the entry record was last modified
  PRIMARY KEY(id), -- Primary key for the 'entered' table
  CONSTRAINT fk_club FOREIGN KEY(club) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(email) REFERENCES users(email) ON UPDATE CASCADE-- Foreign key reference to 'users' table
);

-- Create the 'reservations' table to store reservation information
CREATE TABLE reservations (
  id SERIAL, -- Unique identifier for reservations
  email VARCHAR(32), -- User's name
  club VARCHAR(32), -- Club's name
  date timestamp, -- Start time of the reservation
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the reservation record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the reservation record was last modified
  PRIMARY KEY(id), -- Primary key for the 'reservations' table
  CONSTRAINT fk_club FOREIGN KEY(club) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(email) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE -- Foreign key reference to 'users' table
);

-- Create the 'managers' table to link users with clubs (similar to 'bouncers')
CREATE TABLE managers (
  email VARCHAR(32), -- User's name
  club VARCHAR(32), -- Club's name
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was last modified
  PRIMARY KEY(email), -- Primary key for the 'managers' table
  CONSTRAINT fk_club FOREIGN KEY(club) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(email) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE  -- Foreign key reference to 'users' table
);

-- Create the 'managers' table to link users with clubs (similar to 'bouncers')
CREATE TABLE bouncers (
  email VARCHAR(32), -- User's name
  club VARCHAR(32), -- Club's name
  created_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was created
  last_modified_at timestamp NOT NULL DEFAULT NOW(), -- Timestamp when the manager record was last modified
  PRIMARY KEY(email), -- Primary key for the 'managers' table
  CONSTRAINT fk_club FOREIGN KEY(club) REFERENCES clubs(name) ON UPDATE CASCADE ON DELETE CASCADE, -- Foreign key reference to 'clubs' table
  CONSTRAINT fk_user FOREIGN KEY(email) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE -- Foreign key reference to 'users' table
);

INSERT INTO clubs(name, city, music, capacity, yellow_threshold, current_count) 
VALUES ('Club', 'ROC', 'pop', 3, 2, 2);

INSERT INTO clubs(name, city, music, capacity, yellow_threshold) 
VALUES ('Club Arcane', 'NYC', 'pop', 100, 70);

INSERT INTO clubs(name, city, music, capacity, yellow_threshold ) 
VALUES ('Club Soda','NJ', 'synth', 20, 12);

INSERT INTO clubs(name, city, music, capacity, yellow_threshold ) 
VALUES ('Studio 52','PENN', 'mental', 52, 32);

-- password = admin
INSERT INTO users(name, email, role, password) 
VALUES ('admin', 'admin@rit.edu', 'admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec');

-- password = manager
INSERT INTO users(name, email, role, password) 
VALUES ('manager', 'manager@rit.edu', 'manager', '5fc2ca6f085919f2f77626f1e280fab9cc92b4edc9edc53ac6eee3f72c5c508e869ee9d67a96d63986d14c1c2b82c35ff5f31494bea831015424f59c96fff664');

INSERT INTO managers(email, club) 
VALUES ('manager@rit.edu', 'Club');

-- password = bouncer
INSERT INTO users(name, email, role, password) 
VALUES ('bouncer', 'bouncer@rit.edu', 'bouncer', '58ca118cbe85fb97acc314ebbeff55edbfb089bfdf78f6a2ad7a790cd4e757c3236049a55e27ab2ab23a1a6cfd3f6649b7504b0039ec8ff4d6475a7431660a49');

INSERT INTO bouncers(email, club) 
VALUES ('bouncer@rit.edu', 'Club');


-- password = user
INSERT INTO users(name, email, role, password) 
VALUES ('user1', 'user1@rit.edu', 'user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2');


INSERT INTO entered(email, club, enter_time, left_time, amount_spent) 
VALUES ('user1@rit.edu', 'Club', now(), now(), 100);

-- password = user
INSERT INTO users(name, email, role, password) 
VALUES ('user2', 'user2@rit.edu', 'user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2');

INSERT INTO entered(email, club, enter_time, left_time, amount_spent) 
VALUES ('user2@rit.edu', 'Club', now(), now(), 100);

-- password = user
INSERT INTO users(name, email, role, password) 
VALUES ('user3', 'user3@rit.edu', 'user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2');

INSERT INTO entered(email, club, enter_time, left_time, amount_spent) 
VALUES ('user3@rit.edu', 'Club Arcane', '2022-12-05', '2022-12-05', 100);


-- password = user
INSERT INTO users(name, email, role, password) 
VALUES ('user4', 'user4@rit.edu', 'user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2');

-- password = user
INSERT INTO users(name, email, role, password) 
VALUES ('user5', 'user5@rit.edu', 'user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2');







