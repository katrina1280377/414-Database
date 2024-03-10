SELECT SUM(F.capacity) AS capacity
FROM FLIGHTS F
JOIN MONTHS M ON F.month_id = M.mid
WHERE ((F.origin_city = 'Seattle WA' AND F.dest_city = 'San Francisco CA') OR 
      (F.origin_city = 'San Francisco CA' AND F.dest_city = 'Seattle WA')) AND 
      M.month = 'July' AND 
      F.day_of_month = 10;