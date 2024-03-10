SELECT DISTINCT C.name
FROM FLIGHTS F
JOIN CARRIERS C ON F.carrier_id = C.cid
GROUP BY F.carrier_id, F.month_id, F.day_of_month
HAVING COUNT(F.fid) > 1000;