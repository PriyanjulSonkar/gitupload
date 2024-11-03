import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9a756194f6a1748523c6cfd85823786f&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load movie titles and similarity matrix
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list)  # Convert to DataFrame for easier manipulation
movies_titles = movies_list['title'].values  # Extract titles

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommender(movie):
    # Get the index of the selected movie
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    
    # Get the similarity scores for the selected movie
    distances = similarity[movie_index]
    
    # Get the top 5 most similar movies
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommender_poster = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommender_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommender_poster

# Streamlit app title
st.title('Movie Recommender System')

# Inject CSS into the app
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("background.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    
    .stSelectbox, .stButton {{
        font-size: 18px;
        color: #ffffff;
        background-color: #333333;
        padding: 10px;
        border-radius: 10px;
    }}
    
    .stButton:hover {{
        background-color: #555555;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Dropdown menu to select a movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies_titles,
)

# Button to trigger recommendations
if st.button("Recommend"):
    names, posters = recommender(selected_movie_name)
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])