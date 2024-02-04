SELECT name FROM songs WHERE id IN (SELECT id FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Post Malone'));
