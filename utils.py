import pandas as pd
import bs4 as bs
import requests
import time
from tmdbv3api import Movie
from urllib.request import Request, urlopen
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from api import tmdb
data_url = r"https://res.cloudinary.com/kishanmodi/raw/upload/v1647103420/main_data_kpqadr.csv"


# cosine similarity function (if not created yet)
def create_sim():
    data = pd.read_csv(data_url, sep=",")
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data, sim


def getOttLink(ott_link):
    req = Request(ott_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = bs.BeautifulSoup(webpage, 'lxml')
    ClassS = soup.find_all(
        'ul', {'class': 'providers'})
    link = ClassS[0].find('a')['href']
    return link


def getMovieProviders(id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}/watch/providers?api_key={}'.format(id, tmdb.api_key))
    country_json = response.json()
    try:
        provider_json = country_json['results']['IN']
        ott_link = provider_json['link']
        try:
            ott_link = getOttLink(ott_link)
        except:
            ott_link = ott_link
        flatrate = provider_json['flatrate']
        provider_name = flatrate[0]['provider_name']
        img = flatrate[0]['logo_path']
        logo = 'https://image.tmdb.org/t/p/original{}'.format(img)
        return ott_link, logo
    except:
        pass


def getReviewsFromIMDB(imdbID):
    sauce = urlopen(
        'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdbID)).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    # get user reviews from IMDB site
    soup_result = soup.find_all(
        "div", {"class": "text show-more__control"})

    reviews_list = []  # list of reviews
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
    return reviews_list


def getImdbID(recommendedMovies):
    imdbtime = time.time()
    tmdb_movie = Movie()
    list = []
    for movie in recommendedMovies:
        result = tmdb_movie.search(movie)
        movie_id = result[0].id
        response = requests.get(
            r'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
        data_json = response.json()  # get json data of movies
        imdb_id = data_json['imdb_id']  # get imdb id of movie
        list.append({"id": movie_id, "imdb_id": imdb_id})
    print("--- %s seconds ---" % (time.time() - imdbtime))
    return list


def getYoutubeTrailer(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}/videos?api_key={}'.format(movie_id, tmdb.api_key))
    trailer_json = response.json()
    try:
        for i in range(0, 7):
            if trailer_json['results'][i]['type'] == 'Trailer':
                trailer_link = trailer_json['results'][i]['key']
                trailer_link = 'https://www.youtube.com/embed/{}?vq=hd1080&rel=0&disablekb=1'.format(
                    trailer_link)
                # print(trailer_link)
                return trailer_link
            if trailer_json['results'][i]['type'] == 'Trailer':
                break
    except:
        return None
