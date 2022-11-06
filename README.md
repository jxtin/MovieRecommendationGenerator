# Movie_Recommendation_Discord_Bot 


## Movie Recommendation Discord Bot 

### Enter the exact title of a given movie, and you will be recommended movies according to each movies' overview, popularity and rating 



 Preprocesssing of data [here](https://github.com/jxtin/MovieRecommendationGenerator/blob/master/Movie%20Recommendation/preprocessing.py) 


The TF-IDF approach for 'overview' column and final recommendation functions [here](https://github.com/jxtin/MovieRecommendationGenerator/blob/master/Movie%20Recommendation/overview_recommend.py) 


The [KNN folder](https://github.com/jxtin/MovieRecommendationGenerator/tree/master/KNN) contains code which uses cosine similarity to find distance between two moving using the common genres, cast or keywords indexed and converted to zeros and ones as parameters, it finds the distance of movie with every other movie in datasets and then responds with k (6) nearest neighbors hence the name, K Nearest neighbors. 


### Working of the Recommendation model

![2021-09-19-14-33-26](https://user-images.githubusercontent.com/72869428/133921782-380e812a-43c7-400e-9bfb-0516b33cd490.gif)


### _Download the dataset from [this site](https://www.kaggle.com/tmdb/tmdb-movie-metadata)_ 

### The preprocessed dataset generated for the KNN portion of code can be found [here](https://drive.google.com/drive/folders/1LrAAu-QAjaJ7GGpEvBnMhvOWjvFt6ugm?usp=sharing) 

