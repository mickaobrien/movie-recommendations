for file in output/*.csv
do
  cat "$file"
  #head "$file" -n50
  echo
done > all_movies.csv

#add quotes around titles
sed -i -e "/^$/d; s/^/\"/; s/\,http\:/\"\,http\:/" all_movies.csv

#insert column labels
sed -i '1iname,url,uid,rating' all_movies.csv
