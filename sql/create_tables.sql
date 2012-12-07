# SQL script to create the tables.
CREATE TABLE IF NOT EXISTS Document (
	ID INTEGER,
	title TEXT,
	authors TEXT,
	year INTEGER);

CREATE TABLE IF NOT EXISTS Abstract (
	ID INTEGER,
	year INTEGER,
	abstract TEXT);

CREATE TABLE IF NOT EXISTS Collocation(
	ID INTEGER,
	year INTEGER,
	collocation VARCHAR(64));

CREATE TABLE IF NOT EXISTS Keyword(
	keyword VARCHAR(32),
	year INT,
	ni INT);

CREATE TABLE IF NOT EXISTS Keyword_Doc(
	ID INT,
	year INT,
	keyword VARCHAR(32));

CREATE TABLE IF NOT EXISTS Nouns(
	keyword VARCHAR(32),
	year INT,
	ni INT,
	tag VARCHAR(32));

CREATE TABLE IF NOT EXISTS Nouns_Doc(
	ID INT,
	year INT,
	keyword VARCHAR(32));

CREATE TABLE IF NOT EXISTS Collocation_ni(
	collocation VARCHAR(64),
	year INT,
	ni INT);

CREATE TABLE IF NOT EXISTS Vocabulario(
	keyword VARCHAR(32),
	year INT,
	ni INT);

CREATE TABLE IF NOT EXISTS Posteo(
	ID INT,
	year INT,
	keyword VARCHAR(32));

CREATE TABLE IF NOT EXISTS Cluster(
	year INT,
	k INT,
	cluster_ID INT,
	des_keywords TEXT,
	dis_keywords TEXT);

# Index for tables.
 alter table Document add unique index (ID, year);
 alter table Abstract add unique index (ID, year);
 -- alter table Collocation add unique index (ID, year);

delete from Abstract;
delete from Collocation;
delete from Collocation_ni;
delete from Document;
delete from Keyword;
delete from Keyword_Doc;
delete from Nouns;
delete from Nouns_Doc;
delete from Vocabulario;
delete from Posteo;