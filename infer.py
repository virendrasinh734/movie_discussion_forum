import pandas as pd
import numpy as np
import pickle

# Load user_movie_table from pickle file
with open('user_movie_table.pkl', 'rb') as f:
    user_movie_table = pickle.load(f)

# Load cosine similarity matrix from pickle file
with open('cosine_similarity_matrix.pkl', 'rb') as f:
    cosine_sim_matrix = pickle.load(f)

def get_top_similar_movies(movie_title, user_movie_table, cosine_sim_matrix, n=5):
    # Find the index of the movie in the user_movie_table
    movie_index = user_movie_table.columns.get_loc(movie_title)

    # Calculate cosine similarity between the given movie and all other movies
    sim_scores = cosine_sim_matrix[movie_index]

    # Get indices of top n most similar movies
    top_indices = np.argsort(sim_scores)[-n-1:-1][::-1]

    # Get movie titles corresponding to the indices
    similar_movies = user_movie_table.columns[top_indices]

    return similar_movies

# Example usage
movie_title = user_movie_table[3]
top_similar_movies = get_top_similar_movies(movie_title, user_movie_table, cosine_sim_matrix)
print("Top 5 movies similar to", movie_title, ":", top_similar_movies)
