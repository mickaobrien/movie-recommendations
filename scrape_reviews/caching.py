import os, requests
from hashlib import sha1
from bs4 import BeautifulSoup

# a directory for caching file's we've already downloaded
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

def url_to_filename(url):
    """ Make a URL into a file name, using SHA1 hashes. """

    # use a sha1 hash to convert the url into a unique filename
    hash_file = sha1(url).hexdigest() + '.html'
    return os.path.join(CACHE_DIR, hash_file)


def store_local(url, content):
    """ Save a local copy of the file. """

    # If the cache directory does not exist, make one.
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Save to disk.
    local_path = url_to_filename(url)
    with open(local_path, 'wb') as f:
        f.write(content)


def load_local(url):
    """ Read a local copy of a URL. """
    local_path = url_to_filename(url)
    if not os.path.exists(local_path):
        return None

    with open(local_path, 'rb') as f:
        return f.read()


def get_content(url):
    """ Wrap requests.get() """
    content = load_local(url)
    if content is None:
        #print 'get %s from web' % url
        response = requests.get(url)
        content = response.content
        store_local(url, content)
    return content

def clear_cache(url):
    """ Remove locally cached url. """
    local_path = url_to_filename(url)
    if not os.path.exists(local_path):
        return None

    os.remove(local_path)
    return True

def get_soup(url):
    """ Get soup of cached content. """
    content = get_content(url)
    soup = BeautifulSoup(content)
    return soup
