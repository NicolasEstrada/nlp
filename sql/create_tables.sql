# SQL script to create the tables.
CREATE TABLE Document (
	ID INTEGER,
	title TEXT,
	authors TEXT,
	year INTEGER);

CREATE TABLE Abstract (
	ID INTEGER,
	year INTEGER,
	abstract TEXT);

CREATE TABLE Collocation(
	ID INTEGER,
	year INTEGER,
	collocation VARCHAR(64));

# Index for tables.
 alter table Document add unique index (ID, year);
 alter table Abstract add unique index (ID, year);
 -- alter table Collocation add unique index (ID, year);

