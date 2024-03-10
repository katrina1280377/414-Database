SELECT 
    W.day_of_week AS day_of_week, 
    AVG(F.arrival_delay) AS delay
FROM FLIGHTS F
JOIN WEEKDAYS W ON F.day_of_week_id = W.did
GROUP BY W.day_of_week
LIMIT 1;