combine_files:
    sed -e '$s/$/n/' -s output/*.csv > all_movies.csv

all: combine_files
    sed -i '' -e "s/^/\"/; s/\,http\:/\"\,http\:/" all_movies.csv
    sed -i '1iname,url,uid,rating' all_movies.csv
