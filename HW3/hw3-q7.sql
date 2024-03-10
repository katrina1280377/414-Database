SELECT DISTINCT  C.name AS carrier
FROM CARRIERS C, FLIGHTS F
WHERE C.cid = F.carrier_id AND
      F.origin_city = 'Seattle WA' AND 
      F.dest_city = 'New York NY'
ORDER BY carrier ASC;