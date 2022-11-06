import pandas as pd
import json
import subprocess

df = pd.read_csv("preprocessed.csv")

x = '{"genres":['+ ','.join([i for i in df['genres']])+']}'

data = json.loads(x)

genres_only = pd.Series([],name = "genres_only")
for i in range(len(data["genres"])):
	l = []
	for j in data["genres"][i]:
		l.append(j["name"])
	genres_only[i] = ','.join(l)

df = df.join(genres_only)

genres = set()
for i in df["genres_only"]:
	for genre in i.split(','):
		genres.add(genre)

print(genres)
movie_genres = {}
for find_genre in genres:
	movie_genres[find_genre] = []
	count = 0
	for i in df["genres_only"]:
		if find_genre in i.split(','):
			movie_genres[find_genre].append(count)
		count+=1

df_movies_genre,df_movies_genre_score = {},{}

for genre in movie_genres:
	df_movies_genre[genre] = df.iloc[movie_genres[genre]]
	df_movies_genre[genre].sort_values('score', ascending=False)
	df_movies_genre_score[genre] = []
	for movie in df_movies_genre[genre]["original_title"]:
		if len(df_movies_genre_score[genre])==10:
			break
		try:
			with open("trial.txt","w") as file:
				file.write(movie)
			df_movies_genre_score[genre].append(movie)
		except:
			pass

subprocess.run("del trial.txt",shell = True)

final_movies_score = {}
for genre in movie_genres:
	final_movies_score[genre] = pd.Series(df_movies_genre_score[genre],name = genre)

reco_df = pd.concat([final_movies_score[i] for i in final_movies_score],axis = 1)

reco_df.to_csv("first_timer_score.csv")
