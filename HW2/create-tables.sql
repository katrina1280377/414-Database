CREATE TABLE FLIGHTS (
    fid INT PRIMARY KEY,
    month_id INT,
    day_of_month INT,
    day_of_week_id INT,
    carrier_id VARCHAR(7),
    flight_num INT,
    origin_city VARCHAR(34),
    origin_state VARCHAR(47),
    dest_city VARCHAR(34),
    dest_state VARCHAR(46),
    departure_delay INT,
    taxi_out INT,
    arrival_delay INT,
    canceled INT,
    actual_time INT,
    distance INT,
    capacity INT,
    price INT,
    FOREIGN KEY (carrier_id) REFERENCES CARRIERS (cid),
    FOREIGN KEY (month_id) REFERENCES MONTHS (mid),
    FOREIGN KEY (day_of_week_id) REFERENCES WEEKDAYS (did)
);

CREATE TABLE CARRIERS (cid varchar(7) PRIMARY KEY, name varchar(83));
CREATE TABLE MONTHS (mid int PRIMARY KEY, month varchar(9));
CREATE TABLE WEEKDAYS (did int PRIMARY KEY, day_of_week varchar(9));

PRAGMA foreign_keys=ON;