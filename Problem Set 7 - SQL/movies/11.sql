SELECT title FROM movies JOIN people, stars, ratings
ON movies.id = ratings.movie_id AND movies.id = stars.movie_id AND people.id = stars.person_id
WHERE name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;