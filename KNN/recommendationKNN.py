import pandas as pd
import operator
import warnings
from scipy import spatial


warnings.filterwarnings("ignore")

movies = pd.read_csv("movie recommendations/processedfinalfile.csv")


def tolist(parameter):

    parameter = parameter[1:-1]
    outputlist = parameter.split(", ")
    outputlist = list(map(int, outputlist))

    return outputlist


def Similarity(movieId1, movieId2):
    a = movies.iloc[movieId1]
    b = movies.iloc[movieId2]

    genresA = tolist(a["genres_bin"])
    genresB = tolist(b["genres_bin"])
    genreDistance = spatial.distance.cosine(genresA, genresB)

    scoreA = tolist(a["cast_bin"])
    scoreB = tolist(b["cast_bin"])
    scoreDistance = spatial.distance.cosine(scoreA, scoreB)

    directA = tolist(a["director_bin"])
    directB = tolist(b["director_bin"])
    directDistance = spatial.distance.cosine(directA, directB)

    wordsA = tolist(a["words_bin"])
    wordsB = tolist(b["words_bin"])
    wordsDistance = spatial.distance.cosine(wordsA, wordsB)
    return genreDistance + directDistance + scoreDistance + wordsDistance


new_id = list(range(0, movies.shape[0]))
movies["new_id"] = new_id
movies = movies[
    [
        "original_title",
        "genres",
        "vote_average",
        "genres_bin",
        "cast_bin",
        "new_id",
        "director",
        "director_bin",
        "words_bin",
    ]
]


def getNeighbors(baseMovie, K):
    distances = []

    for index, movie in movies.iterrows():
        if movie["new_id"] != baseMovie["new_id"].values[0]:
            dist = Similarity(baseMovie["new_id"].values[0], movie["new_id"])
            distances.append((movie["new_id"], dist))

    distances.sort(key=operator.itemgetter(1))
    neighbors = []

    for x in range(K):
        neighbors.append(distances[x])
    return neighbors


def predict_score(name):

    new_movie = movies.loc[movies["original_title"] == name]
    print("Selected Movie: ", new_movie.original_title.values[0])

    K = 6
    avgRating = 0
    neighbors = getNeighbors(new_movie, K)
    movrec = "\nRecommended Movies: \n\n"
    print("\nRecommended Movies: \n")
    for neighbor in neighbors:
        avgRating = avgRating + movies.iloc[neighbor[0]][2]
        movrec += (
            str(
                movies.iloc[neighbor[0]][0]
                + " | Rating: "
                + str(movies.iloc[neighbor[0]][2])
            )
            + "\n"
        )

    return movrec
