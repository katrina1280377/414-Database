SELECT origin_city,
    COALESCE(
        CAST(COUNT(CASE WHEN actual_time < 90 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) AS DECIMAL(8, 4)), 
        0
    ) AS percentage
FROM FLIGHTS
WHERE canceled = 0
GROUP BY origin_city
ORDER BY percentage ASC, origin_city ASC;