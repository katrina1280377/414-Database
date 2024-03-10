SELECT C.name,
       SUM(F.arrival_delay) AS delay
FROM   FLIGHTS F
JOIN   CARRIERS C ON F.carrier_id = C.cid
GROUP BY C.name;