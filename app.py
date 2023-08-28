from flask import Flask, request, Response
import json
from flask_cors import CORS
import requests
from rcmdGen import getRecommedations
from utils import getImdbID, getMovieProviders, getYoutubeTrailer, getReviewsFromIMDB
from api import tmdb
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return Response(json.dumps({"Success": True, "Response": 200}), mimetype="application/json")


@app.route("/recommend/")
def recommend():
    import time
    start_time = time.time()
    imdb_id = request.args.get('id')
    response = requests.get(
        r'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(imdb_id, tmdb.api_key))
    data_json = response.json()
    movie = data_json['title']

    recommendedMovies = getRecommedations(movie)
    idList = getImdbID(recommendedMovies)
    print(idList)
    print(type(idList))
    print(recommendedMovies)
    if type(recommendedMovies) == type('string'):  # no such movie found in the database
        returning error message
    return Response(json.dumps({"Success": "False", "Response": 404}), mimetype="application/json")
    else:
        print("--- %s seconds ---" % (time.time() - start_time))
        return Response(json.dumps({"imdb_id": imdb_id, "recommendation": idList, "Success": True, "Response": 200}), mimetype="application/json")


@app.route("/provider/")
def provider():
    try:
        id = request.args.get('id')
        try:
            reviews_list = getReviewsFromIMDB(id)
        except:
            reviews_list = []
        try:
            ott_link, logo = getMovieProviders(id)

        except:
            logo = ""
            ott_link = ""

        youtube_link = getYoutubeTrailer(id)
        print(type(youtube_link))
        if youtube_link == None:
            youtube_link = "None"
        return Response(json.dumps({"id": id, "ott_logo": logo, "youtube_link": youtube_link, "ott_link": ott_link, "reviews": reviews_list, "Success": True, "Response": 200}), mimetype="application/json")
    except:
        return Response(json.dumps({"Success": False, "Response": 404}), mimetype="application/json")


if __name__ == '__main__':
    app.run()
