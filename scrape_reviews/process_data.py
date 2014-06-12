import pandas as pd

def add_movie_id_column():
    """ Add unique movie_id column. """
    movies = pd.read_csv('all_movies.csv')

    # Remove users with only 1 review
    review_counts = movies.groupby('uid').size()
    multiple_reviews = review_counts[review_counts > 1]
    movies = movies[movies['uid'].isin(multiple_reviews.keys())]
    
    # Remove low scores
    movies = movies[movies['rating']>=40]

    # Add unique id for each movie name
    names = movies['name'].unique()
    movie_ids = dict(zip(names, range(len(names))))

    movies['movie_id'] = [movie_ids[name] for name in movies['name']]

    # Write to CSV
    #movies.to_csv('all_movies.csv', index=False)

    # movies
    #movie_df = pd.DataFrame(movie_ids.items(), columns=['title', 'movie_id', 'url'])
    movie_df = movies.drop_duplicates('movie_id')[['name', 'movie_id', 'url']]
    movie_df = movie_df.rename(columns={'name':'title'}) 
    movie_df.to_csv('movies.csv', index=False, encoding='utf-8')

    # users
    unique_users = movies['uid'].unique()
    users_df = pd.DataFrame(data=unique_users, columns=['uid'])
    users_df.to_csv('users.csv', index=False)

    # ratings
    movies[['uid', 'rating', 'movie_id']].to_csv('ratings.csv', index=False)

if __name__ == '__main__':
    add_movie_id_column()
