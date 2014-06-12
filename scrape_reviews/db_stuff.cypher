USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "./final_data/movies.csv" AS csvline
CREATE (movie:Movie { mid: toInt(csvline.movie_id), title: csvline.title, url: csvline.url, trailer: csvline.trailer });

CREATE INDEX ON :Movie(mid);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "./final_data/users.csv" AS csvline
CREATE (user:User { uid: toInt(csvline.uid) });

CREATE INDEX ON :User(uid);


USING PERIODIC COMMIT 100
LOAD CSV WITH HEADERS FROM "./final_data/ratings.csv" AS csvline
MATCH (u:User), (m:Movie)
WHERE u.uid = toInt(csvline.uid) AND m.mid = toInt(csvline.movie_id)
MERGE((u)-[r:RATED { rating: toInt(csvline.rating) }]->(m));
