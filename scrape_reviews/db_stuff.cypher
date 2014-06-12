USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///home/michael/Dropbox/dev/data-works/movie-recommender/scrape_reviews/movies.csv" AS csvline
CREATE (movie:Movie { mid: toInt(csvline.movie_id), title: csvline.title, url: csvline.url, trailer: csvline.trailer });

CREATE INDEX ON :Movie(mid);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///home/michael/Dropbox/dev/data-works/movie-recommender/scrape_reviews/users.csv" AS csvline
CREATE (user:User { uid: toInt(csvline.uid) });

CREATE INDEX ON :User(uid);


USING PERIODIC COMMIT 100
//LOAD CSV WITH HEADERS FROM "file:///home/michael/Dropbox/dev/data-works/movie-recommender/scrape_reviews/short_ratings.csv" AS csvline
LOAD CSV WITH HEADERS FROM "file:///home/michael/Dropbox/dev/data-works/movie-recommender/scrape_reviews/ratings.csv" AS csvline
MATCH (u:User), (m:Movie)
WHERE u.uid = toInt(csvline.uid) AND m.mid = toInt(csvline.movie_id)
MERGE((u)-[r:RATED { rating: toInt(csvline.rating) }]->(m));
//./bin/neo4j-shell -c < ~/Dropbox/dev/data-works/movie-recommender/scrape_reviews/db_stuff.cypher

//WITH [1469,847] AS movies
//MATCH (u)-[r:RATED]->(m)
//WHERE m.mid IN movies
//WITH u, movies, COUNT(r) AS c
//MATCH (u)-[r1]->(m1)
//WHERE NOT(m1.mid IN movies)
//WITH m1, SUM(c*r1.rating)/COUNT(r1) AS total
//RETURN m1.title, total
//ORDER BY total DESC
//LIMIT 100
