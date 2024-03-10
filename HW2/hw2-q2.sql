SELECT C.name AS name,
       F1.flight_num AS f1_flight_num,
       F1.origin_city AS f1_origin_city,
       F1.dest_city AS f1_dest_city,
       F1.actual_time AS f1_actual_time,
       F2.flight_num AS f2_flight_num,
       F2.origin_city AS f2_origin_city,
       F2.dest_city AS f2_dest_city,
       F2.actual_time AS f2_actual_time,
       F1.actual_time + F2.actual_time AS actual_time
FROM FLIGHTS F1 
JOIN FLIGHTS F2 ON F1.carrier_id = F2.carrier_id AND
     F1.dest_city = F2.origin_city AND
     F1.day_of_month = F2.day_of_month
JOIN MONTHS M ON F1.month_id = M.mid
JOIN CARRIERS C ON F1.carrier_id = C.cid
WHERE F1.origin_city = 'Seattle WA' AND
      F2.dest_city = 'Boston MA' AND
      M.month  = 'July' AND
      F1.day_of_month = 15 AND
      F1.actual_time + F2.actual_time < 420;