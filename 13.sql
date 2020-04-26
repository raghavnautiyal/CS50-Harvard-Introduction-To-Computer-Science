SELECT DISTINCT (name) FROM people
WHERE name IS NOT 'Kevin Bacon'
AND id IN
(SELECT person_id FROM stars Where movie_id IN
(SELECT movie_id FROM stars Where person_id IN
(SELECT id FROM people WHERE name IS 'Kevin Bacon' and birth = 1958)))
ORDER BY name;