# Movie Recommendation System


## Deployed on discord as a bot 

### Enter the exact title of a given movie, and you will be recommended movies according to each movies' overview, popularity and rating 



 Preprocesssing of data is linked: [here](https://github.com/jxtin/MovieRecommendationGenerator/blob/master/Movie%20Recommendation/preprocessing.py) 


The TF-IDF approach for 'overview' column and final recommendation functions is linked here: [here](https://github.com/jxtin/MovieRecommendationGenerator/blob/master/Movie%20Recommendation/overview_recommend.py) 


The [KNN folder](https://github.com/jxtin/MovieRecommendationGenerator/tree/master/KNN) contains code which uses cosine similarity to find distance between two movies using their common genres, cast or keywords indexed and converted to zeros and ones as parameters. It then finds the distance of the entered movie with every other movie in the concerned datasets to respond with k (6) nearest neighbors: hence the name, K Nearest neighbors. 


### Working of the Recommendation model

![2021-09-19-14-33-26](https://user-images.githubusercontent.com/72869428/133921782-380e812a-43c7-400e-9bfb-0516b33cd490.gif)


### _Download the dataset from: [this site](https://www.kaggle.com/tmdb/tmdb-movie-metadata)_ 

### The preprocessed dataset generated for the KNN portion of code is linked: [here](https://drive.google.com/drive/folders/1LrAAu-QAjaJ7GGpEvBnMhvOWjvFt6ugm?usp=sharing) 

