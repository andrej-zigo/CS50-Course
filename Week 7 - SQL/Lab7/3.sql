SELECT name FROM songs GROUP BY duration_ms ORDER BY COUNT(*) DESC LIMIT 5;
