import json

import pandas as pd
import numpy as np
import json


movies = pd.read_csv("processedfinalfile.csv")
movies.head()


from scipy import spatial


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


import operator


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
    # name = input('Enter a movie title: ')
    new_movie = movies.loc[movies["original_title"] == name]
    # print('Selected Movie: ',new_movie.original_title.values[0])

    K = 6
    avgRating = 0
    neighbors = getNeighbors(new_movie, K)

    return neighbors


def predict_score_byid(new_id):
    # name = input('Enter a movie title: ')
    new_movie = movies.loc[movies["new_id"] == new_id]
    print("Selected Movie: ", new_movie.original_title.values[0])

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

    K = 6
    avgRating = 0
    neighbors = getNeighbors(new_movie, K)

    return neighbors


mov2recommendations = {}
n = 0
for movie in movies["original_title"]:
    print(movie, m)
    listofrecommendations = []
    neighbors = predict_score(movie)
    for neighbor in neighbors:
        # print(neighbor)
        listofrecommendations.append((movies.iloc[neighbor[0]])["original_title"])
    # print(listofrecommendations)
    mov2recommendations[movie] = listofrecommendations
    n = n + 1
    if n % 50 == 0:
        print("precautionary merging and printing")
        print(mov2recommendations)
        with open(f"merged_testing_new.json", "w") as outfile:
            json.dump(mov2recommendations, outfile)
