var express =  require('express');
var rec = require('./recommend');
var app = express();

var hbs = require('hbs');
hbs.registerHelper("listing", function(movie, options) {
        var ret = "<li class='movie'>";

        function link(text, address) {
            return [" <a href='",
                    address,
                    "'>",
                    text,
                    "</a>"].join("");
        }

        ret += movie.title;

        ret += " :: ";
        ret += link("More Info", movie.url);

        // Add trailer link if it exists
        if (movie.trailer==="true") {
            ret += [" - ",
                    link("Trailer", movie.url+"trailer/")].join("");
        }
        return ret;
    });

app.set('view engine', 'html');
app.engine('html', hbs.__express);

app.use(express.static('public'));

app.get('/', function(req, res) {
    res.sendfile('./views/index.html');
});


app.get('/recommendations/*', function(req, res) {
    var movieIDs = req.query.mid;
    if (typeof(movieIDs)==='string') {
        movieIDs = [movieIDs];
    }

    if (movieIDs.length > 3) {
        res.render('movies', {error: "Too many movies chosen."})
    }

    var movies = movieIDs.map(function(n) { return parseInt(n, 10); });
    var output = function(result) { 
        //res.render('movies', {movies: result});
        res.render('movies', result);
    };
    recommendations = rec.getRecommendations({'movie_ids': movies}, output);
});

app.listen(3000);
