SELECT DISTINCT F1.origin_city AS city
FROM FLIGHTS F1
WHERE NOT EXISTS(
        SELECT actual_time
        FROM FLIGHTS F2
        WHERE F1.origin_city = F2.origin_city AND 
              F2.actual_time >= 240
    )
ORDER BY city ASC;