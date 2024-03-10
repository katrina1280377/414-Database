SELECT DISTINCT
       F1.origin_city, 
       F1.dest_city, 
       F1.actual_time AS time
FROM FLIGHTS F1, (
        SELECT origin_city, 
               MAX(actual_time) AS max_time
        FROM FLIGHTS
        GROUP BY origin_city
    ) F2
WHERE F1.origin_city = F2.origin_city AND F1.actual_time = F2.max_time
ORDER BY F1.origin_city ASC, F1.dest_city ASC;