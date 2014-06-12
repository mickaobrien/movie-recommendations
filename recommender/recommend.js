var neo4j = require('neo4j');
var db = new neo4j.GraphDatabase('http://localhost:7474');

exports.getRecommendations = function(movie_ids, callback) {
    var query = [
        'WITH {movie_ids} AS movies',
        'MATCH (u)-[r]->(m)',
        'WHERE m.mid IN movies',
        'WITH u, movies, COUNT(r) AS c',
        'MATCH (u)-[r1]->(m1)',
        'WHERE NOT(m1.mid IN movies)',
        'WITH m1, SUM(c*r1.rating) AS total',
        'RETURN m1.title AS title, m1.url AS url, m1.trailer AS trailer',
        'ORDER BY total DESC',
        'LIMIT 10'
        ].join('\n');

    db.query(query, movie_ids, function(err, results) {
        if (err) {
            callback({error: "Oops! Something went wrong, please try again."});
        }
        callback({movies: results});
    });

}

