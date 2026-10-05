QUERY students
FROM "students.json"
WHERE age >= 20 AND cgpa > 8.0
SELECT name, age, cgpa
SORT BY cgpa DESC
LIMIT 3
