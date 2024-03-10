SELECT DISTINCT C.name AS carrier
FROM CARRIERS C
WHERE C.cid IN (
        SELECT F.carrier_id
        FROM FLIGHTS F
        WHERE 
            F.origin_city = 'Seattle WA' AND 
            F.dest_city = 'New York NY'
    )
ORDER BY carrier ASC;