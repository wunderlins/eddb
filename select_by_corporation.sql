SELECT sy.name system, s.name station, s.distance_to_star, s.faction, s.government, s.allegiance,
       julianday('now')-julianday(datetime(s.updated_at, 'unixepoch', 'localtime')) last_upd_days_ago
FROM station s LEFT JOIN system sy ON (s.system_id = sy.id) 
WHERE s.faction like '%sirius%'
  AND s.max_landing_pad_size = 'L'
  AND s.distance_to_star < 2000;
