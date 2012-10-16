# SQL script to create the tables.
CREATE TABLE Document (
	ID INTEGER,
	title VARCHAR(255),
	authors VARCHAR(255),
	year INTEGER);

CREATE TABLE Abstract (
	ID INTEGER,
	year INTEGER,
	abstract VARCHAR(255));

CREATE TABLE Collocation(
	ID INTEGER,
	year INTEGER,
	collocation VARCHAR(64));

# Index for tables.
 alter table Document add unique index (ID, year);
 alter table Abstract add unique index (ID, year);
 alter table Collocation add unique index (ID, year);

