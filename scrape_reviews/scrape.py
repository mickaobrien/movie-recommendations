import re, os
from caching import get_soup

BASE_URL = 'http://www.rottentomatoes.com'

def get_data():
    bestofs = get_bestof_links()

    all_movie_data = []

    for link in bestofs[10:]:
        movies = get_movie_links(link)

        for movie in movies:
            info = get_movie_info(movie)
            filename = 'output/%s.csv' % info[0].replace(' ', '').replace('/', '')

            if os.path.exists(filename):
                print '%s already exists...' % filename

            else:
                print 'Getting reviews for %s' % info[0]
                reviews = get_audience_reviews(movie)
                movie_data = [info + r for r in reviews]
                write_to_csv(filename, movie_data)

            print ''
            #all_movie_data += movie_data

    #return all_movie_data

def write_to_csv(filename, data):
    with open(filename, 'w') as f:
        f.write('\n'.join('%s,%s,%d,%d' % d for d in data))
    print 'Written to file %s' % filename

def get_bestof_links():
    soup = get_soup('http://www.rottentomatoes.com/top/')
    links = soup.findAll('a', href=re.compile('/top/bestofrt.*'))

    # Filter out view all link duplicates
    links = [BASE_URL + l['href'] for l in links if not l.text.startswith('View')]

    return links

def get_movie_links(bestof_url):
    soup = get_soup(bestof_url)
    links = soup.find('div', {'id': 'top_movies_main'}).findAll('a')

    links = [BASE_URL + l['href'] for l in links]

    return links

def get_movie_info(movie_url):
    soup = get_soup(movie_url)
    title = soup.find('h1', {'class': 'movie_title'}).text.encode('utf8')

    return (title, movie_url)

def get_audience_reviews(movie_url):
    reviews_url = movie_url + 'reviews/?type=user'
    soup = get_soup(reviews_url)

    info = soup.find('span', {'class': 'pageInfo'}).text
    num_pages = int(info.split('of ')[1])

    upper = min(52, num_pages)

    all_reviews = []

    for page in range(1, upper+1):
        review_page = '%s&page=%d' % (reviews_url, page)
        all_reviews += parse_review_page(review_page)

    deduped = list(set(all_reviews))

    return deduped

def parse_review_page(review_page_url):
    soup = get_soup(review_page_url)
    reviews_div = soup.find('div', {'id': 'reviews'})

    if not reviews_div:
        return []

    reviews = reviews_div.findAll('div', {'class': 'bottom_divider'})
    
    results = [parse_review(review) for review in reviews]
    clean_results = [r for r in results if r is not None]

    return clean_results

def parse_review(review):
    uid = int(review.find('div', {'class': 'name'}).a['href'].split('/')[-2])
    star_span = review.find('span', {'class': 'rating'})

    if not star_span:
        return None

    classes = star_span.attrs['class']
    score = [c for c in classes if c.startswith('score')]

    if score:
        rating = int(score[0][-2:])
        return (uid, rating)
    else:
        return None
