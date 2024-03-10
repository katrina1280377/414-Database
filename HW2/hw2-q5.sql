SELECT C.name AS name, 
       (CAST(SUM(CASE WHEN F.canceled = 1 THEN 1 ELSE 0 END) AS FLOAT) / CAST(COUNT(F.fid) AS FLOAT)) * 100 AS percentage
FROM FLIGHTS F
JOIN CARRIERS C ON F.carrier_id = C.cid
WHERE F.origin_city = 'Seattle WA'
GROUP BY C.name
HAVING percentage > 0.5
ORDER BY percentage ASC;