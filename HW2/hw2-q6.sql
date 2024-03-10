SELECT C.name AS carrier, 
       MAX(F.price) AS max_price
FROM FLIGHTS F
JOIN CARRIERS C ON F.carrier_id = C.cid
WHERE (F.origin_city = 'Seattle WA' AND F.dest_city = 'New York WA') OR 
      (F.origin_city = 'New York NY' AND F.dest_city = 'Seattle WA')
GROUP BY C.name;