import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")
import json
import warnings
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")

# creating pandas dataframes for the datasets to be used

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# changing the genres column from json to string
movies["genres"] = movies["genres"].apply(json.loads)
for index, i in zip(movies.index, movies["genres"]):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]["name"]))  # the key 'name' contains the name of the genre
    movies.loc[index, "genres"] = str(list1)

# changing the keywords column from json to string
movies["keywords"] = movies["keywords"].apply(json.loads)
for index, i in zip(movies.index, movies["keywords"]):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]["name"]))
    movies.loc[index, "keywords"] = str(list1)

# changing the production_companies column from json to string
movies["production_companies"] = movies["production_companies"].apply(json.loads)
for index, i in zip(movies.index, movies["production_companies"]):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]["name"]))
    movies.loc[index, "production_companies"] = str(list1)

# changing the cast column from json to string
credits["cast"] = credits["cast"].apply(json.loads)
for index, i in zip(credits.index, credits["cast"]):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]["name"]))
    credits.loc[index, "cast"] = str(list1)

# changing the crew column from json to string
credits["crew"] = credits["crew"].apply(json.loads)


def director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]


credits["crew"] = credits["crew"].apply(director)
credits.rename(columns={"crew": "director"}, inplace=True)


# Merging the two datasets, movies.csv and credits.csv keeping id/movie id common
movies = movies.merge(credits, left_on="id", right_on="movie_id", how="left")
movies = movies[
    ["id", "original_title", "genres", "cast", "vote_average", "director", "keywords"]
]

# converting movie genres column to list by removing brackets and splitting by commas

movies["genres"] = (
    movies["genres"].str.strip("[]").str.replace(" ", "").str.replace("'", "")
)
movies["genres"] = movies["genres"].str.split(",")

for i, j in zip(movies["genres"], movies.index):
    list2 = []
    list2 = i
    list2.sort()
    movies.loc[j, "genres"] = str(list2)
movies["genres"] = (
    movies["genres"].str.strip("[]").str.replace(" ", "").str.replace("'", "")
)
movies["genres"] = movies["genres"].str.split(",")

# creating a list of genres by searching and adding all unique genres throughout the coluumn

genreList = []
for index, row in movies.iterrows():
    genres = row["genres"]

    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)
genreList[:10]  # now we have a list with unique genres


# creating a list of zeros for each movie and setting them 1 if the genre of that particular index is found


def binary(genre_list):
    binaryList = []

    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


movies["genres_bin"] = movies["genres"].apply(lambda x: binary(x))


# converting movie cast column to list by removing brackets and splitting by commas


movies["cast"] = (
    movies["cast"]
    .str.strip("[]")
    .str.replace(" ", "")
    .str.replace("'", "")
    .str.replace('"', "")
)
movies["cast"] = movies["cast"].str.split(",")

# creating a list of cast by searching and adding all unique genres throughout the coluumn


for i, j in zip(movies["cast"], movies.index):
    list2 = []
    list2 = i[:4]
    movies.loc[j, "cast"] = str(list2)
movies["cast"] = (
    movies["cast"].str.strip("[]").str.replace(" ", "").str.replace("'", "")
)
movies["cast"] = movies["cast"].str.split(",")

castList = []
for index, row in movies.iterrows():
    cast = row["cast"]

    for i in cast:
        if i not in castList:
            castList.append(i)


# creating a list of zeros for each movie and setting them 1 if the cast of that particular index is found


def binary(cast_list):
    binaryList = []

    for genre in castList:
        if genre in cast_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


movies["cast_bin"] = movies["cast"].apply(lambda x: binary(x))

# to set none values in directors column to empty string


def xstr(s):
    if s is None:
        return ""
    return str(s)


movies["director"] = movies["director"].apply(xstr)

# creating a list of director by searching and adding all unique genres throughout the coluumn

directorList = []
for i in movies["director"]:
    if i not in directorList:
        directorList.append(i)


# creating a list of zeros for each movie and setting them 1 if the director of that particular index is found


def binary(director_list):
    binaryList = []
    for direct in directorList:
        if direct in director_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList


movies["director_bin"] = movies["director"].apply(lambda x: binary(x))


# using nltk to tokenize words in the keywords column and creating their list and removing punctuations of all sorts

stop_words = set(stopwords.words("english"))
stop_words.update(",", ";", "!", "?", ".", "(", ")", "$", "#", "+", ":", "...", " ", "")

words = movies["keywords"].dropna().apply(nltk.word_tokenize)
word = []
for i in words:
    word.extend(i)
word = pd.Series(word)
word = [i for i in word.str.lower() if i not in stop_words]
wc = WordCloud(
    background_color="black",
    max_words=2000,
    stopwords=STOPWORDS,
    max_font_size=60,
    width=1000,
    height=1000,
)

movies["keywords"] = (
    movies["keywords"]
    .str.strip("[]")
    .str.replace(" ", "")
    .str.replace("'", "")
    .str.replace('"', "")
)
movies["keywords"] = movies["keywords"].str.split(",")


for i, j in zip(movies["keywords"], movies.index):
    list2 = []
    list2 = i
    movies.loc[j, "keywords"] = str(list2)
movies["keywords"] = (
    movies["keywords"].str.strip("[]").str.replace(" ", "").str.replace("'", "")
)
movies["keywords"] = movies["keywords"].str.split(",")
for i, j in zip(movies["keywords"], movies.index):
    list2 = []
    list2 = i
    list2.sort()
    movies.loc[j, "keywords"] = str(list2)
movies["keywords"] = (
    movies["keywords"].str.strip("[]").str.replace(" ", "").str.replace("'", "")
)
movies["keywords"] = movies["keywords"].str.split(",")


words_list = []
for index, row in movies.iterrows():
    genres = row["keywords"]

    for genre in genres:
        if genre not in words_list:
            words_list.append(genre)

# creating a list of zeros for each movie and setting them 1 if the keywords of that particular index is found


def binary(words):
    binaryList = []
    for genre in words_list:
        if genre in words:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList


# Creating keyword binaries
movies["words_bin"] = movies["keywords"].apply(lambda x: binary(x))

# Removing movies with 0 score and without drector names
movies = movies[(movies["vote_average"] != 0)]
movies = movies[movies["director"] != ""]

# saving finaldatabase as processedfinalfile.csv

movies.to_csv("processedfinalfile.csv")
