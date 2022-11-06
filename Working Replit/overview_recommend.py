import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

movies_preprocessed = pd.read_csv("preprocessed.csv")

tfv = TfidfVectorizer(min_df=3,
                      max_features=None,
                      strip_accents='unicode',
                      analyzer='word',
                      token_pattern=r'\w{1,}',
                      ngram_range=(1, 3),
                      stop_words='english')

movies_preprocessed['overview'] = movies_preprocessed['overview'].fillna('')

tfv_matrix = tfv.fit_transform(movies_preprocessed['overview'])

sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

# Reverse mapping of indices and movie titles
indices = pd.Series(
    movies_preprocessed.index,
    index=movies_preprocessed['original_title']).drop_duplicates()


def give_title_score(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 20 most similar movies
    sig_scores = sig_scores[1:21]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 20 similar movies
    sig_df = movies_preprocessed[['original_title', 'score']].iloc[movie_indices]
    return_df = sig_df.sort_values('score', ascending=False)

	# Top 10 good weighted average movies which are similar
    return_movies = [list(row)[0] for row in return_df[:10].values]
    return return_movies

def give_only_title(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 similar movies
    return_df = movies_preprocessed[['original_title', 'score']].iloc[movie_indices]

	# Final Movies list
    return_movies = [list(row)[0] for row in return_df[:10].values]
    return return_movies


