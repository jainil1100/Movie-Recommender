import streamlit as st
import pickle
import pandas as pd
import base64

# Function to set background
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("Film Poster 1.jpg")

# Load movies and similarity matrix
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load similarity matrix

# Function for genre-based recommendation
def recommend_by_genre(selected_genre, num_recommendations=7):
    genre_movies = movies[movies['tags'].str.contains(selected_genre, case=False, na=False)]
    if genre_movies.empty:
        return [f"No movies found with the tag: {selected_genre}."]
    
    recommended_movies = genre_movies.sample(n=min(num_recommendations, len(genre_movies)), random_state=42)
    return recommended_movies['title'].tolist()

# Function for similarity-based recommendation
def recommend_by_movie(movie_title, num_recommendations=5):
    if movie_title not in movies['title'].values:
        return [f"Movie '{movie_title}' not found in the database."]
    
    index = movies[movies['title'] == movie_title].index[0]  # Get movie index
    similar_movies = list(enumerate(similarity[index]))  # Get similarity scores
    sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]  # Sort

    recommended_movies = [movies.iloc[i[0]]['title'] for i in sorted_movies]
    return recommended_movies

# Streamlit UI
st.title("🎬 Movie Recommender System")

# Tabs for different recommendation methods
option = st.radio("Choose recommendation type:", ["By Genre", "By Similarity"])

if option == "By Genre":
    st.subheader("Genre-Based Recommendation")
    selected_genre = st.text_input("Enter a genre (e.g., Thriller, Action, Comedy):")
    num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=49, value=5)

    if st.button("Recommend by Genre"):
        recommendations = recommend_by_genre(selected_genre, num_recommendations)
        st.write(f"### Movies in '{selected_genre}' Genre:")
        for movie in recommendations:
            st.write(f"- **{movie}**")

elif option == "By Similarity":
    st.subheader("Movie-Based Recommendation")
    selected_movie = st.text_input("Enter a movie title:")
    num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=10, value=5)

    if st.button("Recommend Similar Movies"):
        recommendations = recommend_by_movie(selected_movie, num_recommendations)
        st.write(f"### Movies similar to '{selected_movie}':")
        for movie in recommendations:
            st.write(f"- **{movie}**")
