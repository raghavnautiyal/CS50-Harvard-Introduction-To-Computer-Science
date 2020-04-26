SELECT DISTINCT name FROM people 
JOIN movies, directors, ratings 
ON movies.id = ratings.movie_id AND movies.id = directors.movie_id AND people.id = directors.person_id 
WHERE rating >= 9.0;