-- created a gym database.
CREATE DATABASE gym; 


use gym;

-- create a both a members table and workoutsession table.
	-- members table host the gentic inform about the person.
	-- workout session table host the workout program fro each memeber in the members table.
		-- link is establish through a foreign key.

CREATE TABLE members (
id int AUTO_INCREMENT PRIMARY KEY,
member_name VARCHAR(75) NOT NULL,
phone VARCHAR(16) NULL
);

CREATE TABLE workoutsessions (
id INT AUTO_INCREMENT PRIMARY KEY,
workout_type VARCHAR(150) NOT NULL,
duration VARCHAR(150) NULL,
members_id INT,
FOREIGN KEY (members_id) REFERENCES members(id)
); -- relationship between members and workout sessions

-- to test tables were hosting data correct, members and workout programs were implemented.
	-- along with a fetch all SQL command to verfiy the contents before database connection is made.

-- inserting names into members table

INSERT INTO members (member_name,phone)
VALUES('Tom', '5554443333'), 
('Tim','3335554444'), ('Bob','8889995656'), 
('Jill','7775852222'), ('Liz','3336589999'); 

SELECT * FROM members;

-- inserting workout routines 

INSERT INTO workoutsessions(workout_type, duration, members_id)
VALUES('cardio', '60 mins', 1),
('weights', '90 mins', 2),
('cardio', '30 mins', 3),
('pilates', '120 mins', 4),
('cardio', '30 mins', 1),
('weights', '60 mins', 5); 

SELECT  * FROM workoutsessions;

-- Below is a fail safe to drop all tables if data is corrupted.
	-- ONLY USE IF NECCESSARY.

-- DROP TABLE workoutsessions;
-- DROP TABLE members;
