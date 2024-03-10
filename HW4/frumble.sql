-- a. Create a table
CREATE TABLE SALES (
    name VARCHAR(256),
    discount VARCHAR(256),
    month VARCHAR(256),
    price INTEGER
);

-- b. Find all non-trivial FD in the database.
-- 1. month -> discount
-- There is 0 result, FD holds
SELECT *
FROM SALES S1, SALES S2
WHERE S1.month = S2.month AND 
      S1.discount != S2.discount;

-- 2. name->price
-- There is 0 result, FD holds
SELECT *
FROM SALES S1, SALES S2
WHERE S1.name = S2.name AND 
      S1.price != S2.price;

-- 3. name->discount
-- There are 3286 results, which means FD doesn't hold
SELECT *
FROM SALES S1, SALES S2
WHERE S1.name = S2.name AND 
      S1.discount != S2.discount;

-- c. Decompose the table into BCNF
-- R(name,discount,month,price)
-- R1(month,discount)
-- R2(name,price) 
-- R3(name,month)
CREATE TABLE R1(
    month VARCHAR(256) primary key,
    discount VARCHAR(256)
);
CREATE TABLE R2(
    name VARCHAR(256) primary key,
    price INTEGER
);
CREATE TABLE R3(
    name VARCHAR(256),
    month VARCHAR(256),
    FOREIGN KEY (month) REFERENCES R1(month),
    FOREIGN KEY (name) REFERENCES R2(name)
);

-- d. Turn in the SQL queries and comment the size of the tables after loading them
-- 13 rows
INSERT INTO R1(month, discount)
SELECT DISTINCT month, discount
FROM SALES;

SELECT COUNT(*) 
FROM R1;

-- 37 rows
INSERT INTO R2(name, price)
SELECT DISTINCT name, price
FROM SALES;

SELECT COUNT(*) 
FROM R2;

-- 427 rows
INSERT INTO R3(name, month)
SELECT DISTINCT name, month
FROM SALES;

SELECT COUNT(*)
FROM R3;
