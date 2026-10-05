QUERY high_performers
FROM "students.json"
WHERE (cgpa >= 9.0 OR age >= 23) AND NOT age < 20
SELECT name, age, cgpa
SORT BY age ASC
LIMIT 10
