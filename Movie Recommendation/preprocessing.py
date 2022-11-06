
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#https://www.kaggle.com/tmdb/tmdb-movie-metadata
credits = pd.read_csv("tmdb_5000_credits.csv")

movies_df = pd.read_csv("tmdb_5000_movies.csv")

#merging the datasets based on their movie_id so that a single dataset is combined out of the two
credits_column_renamed = credits.rename(index=str, columns={"movie_id": "id"})
movies_df_merge = movies_df.merge(credits_column_renamed, on='id')

# Unnecessary columns are dropped
movies_cleaned_df = movies_df_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status','production_countries'])

# Values based on whicht the weighted average will be calculated are set here
v=movies_cleaned_df['vote_count']
R=movies_cleaned_df['vote_average']
C=movies_cleaned_df['vote_average'].mean()
m=movies_cleaned_df['vote_count'].quantile(0.80)

# THe weighted average is set for each movie 
movies_cleaned_df['weighted_average']=((R*v)+ (C*m))/(v+m)

# DataFrame sorted with weighted_average as the key
weight_average=movies_cleaned_df.sort_values('weighted_average',ascending=False)

# DataFrame sorted with popularity as the key
popularity=movies_cleaned_df.sort_values('popularity',ascending=False)

# Scaling together the weighted_average and popularity keys based on which the final score will be decided
scaling=MinMaxScaler()

# Values are normalized here essentially
movie_scaled_df=scaling.fit_transform(movies_cleaned_df[['weighted_average','popularity']])

movie_normalized_df=pd.DataFrame(movie_scaled_df,columns=['weighted_average','popularity'])

movies_cleaned_df[['normalized_weight_average','normalized_popularity']]= movie_normalized_df

# The final score: poularity and weighted average are given equal importance in this case and hence 0.5 is the factor for each
movies_cleaned_df['score'] = movies_cleaned_df['normalized_weight_average'] * 0.5 + movies_cleaned_df['normalized_popularity'] * 0.5

# Arranging the csv file based score
scored_df = movies_cleaned_df.sort_values('score', ascending=False)

# Saving the processed csv for further usage
scored_df.to_csv("preprocessed.csv")
