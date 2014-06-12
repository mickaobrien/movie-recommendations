import pandas as pd

movies = pd.read_csv('../final_data/movies.csv')
movies['s_title'] = [t.lower() for t in movies['title']]

movies = movies.sort('s_title')

mvs = zip(movies['movie_id'], movies['title'])

opts = []
for movie in mvs:
    opts.append('<option value="%d">%s</option>' % movie)

with open('options.html', 'w') as f:
    f.write('\n'.join(opts))
