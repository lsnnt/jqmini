QUERY access
FROM "fixed.json"
WHERE level='info'
SELECT ts,logger
LIMIT 10