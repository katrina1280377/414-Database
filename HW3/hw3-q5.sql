SELECT DISTINCT F3.dest_city AS city
FROM FLIGHTS F1, FLIGHTS F2, FLIGHTS F3
WHERE
    F1.dest_city = F2.origin_city AND
    F2.dest_city = F3.origin_city AND
    F1.origin_city = 'Seattle WA' AND 
    F2.dest_city <> 'Seattle WA' AND 
    F2.dest_city NOT IN (
        SELECT dest_city
        FROM FLIGHTS
        WHERE origin_city = 'Seattle WA'
    ) AND 
    F3.dest_city NOT IN (
        SELECT F2.dest_city
        FROM FLIGHTS F1, FLIGHTS F2
        WHERE 
            F1.dest_city = F2.origin_city AND
            F1.origin_city = 'Seattle WA'
	)
ORDER BY city ASC;