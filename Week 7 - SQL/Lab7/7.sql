SELECT AVG(DISTINCT(energy)) AS average_energy FROM songs WHERE id IN (SELECT id FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Drake'));
