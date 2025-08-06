import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

file_path = "similarity.pkl"
if not os.path.exists(file_path):
    # Replace the URL below with your own shared link
    simi = "https://drive.google.com/uc?id=1A5Hlx-kzQcPyVejmy113KATkHGMJrcV9"
    gdown.download(simi, file_path, quiet=False)



# def fetch_poster(movie_id):
#     response = requests.get(
#         'https://api.themoviedb.org/3/movie/{}?api_key=7a90e1fec3f1a3082b060c1fac54ae4e&language=en-US'.format(
#             movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
@st.cache_data(ttl=3600)  # cache result for 1 hour
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7a90e1fec3f1a3082b060c1fac54ae4e&language=en-US'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        print(f"Error: {e}")
        return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movie_dic.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('🎬 Movie Recommender System')
selected_movie_name = st.selectbox(
    'How would you like to recommend movies?',
    movies['title'].values)
if st.button('Recommended Movies'):
    names,posters  = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
