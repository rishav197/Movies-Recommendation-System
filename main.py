import streamlit as st
import pandas as pd
import pickle
import requests

st.title('Movies Recommender System')


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('Cosine_Similarity_Model/similarity.pkl','rb'))




def fetch_posterfromAPI(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f7782363e180b6076266a7f224b00e09&language=en-US'.format(movie_id))
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie):
    movie_idx = movies[movies['title']==movie].index[0]
    distances = similarity[movie_idx]
    movies_lst = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:7]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_lst:
        
        recommended_movies.append(movies.iloc[i[0]].title)

        #fetch poster from tmdb API
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_posterfromAPI(movie_id))

    return recommended_movies, recommended_movies_posters



# Select Box 
selected_movie_names = st.selectbox('Type or select a movie from the dropdown', 
movies['title'].values)

# Submit button and Layout of the Recommender's page
if st.button('Submit'):
    # now, we get names and poster paths of each recommended movie
    names, poster_paths = recommend(selected_movie_names)
    
    col0, col1, col2, col3, col4, col5 = st.columns(6)
    with col0:
        st.text(names[0])
        st.image(poster_paths[0])

    with col1:
        st.text(names[1])
        st.image(poster_paths[1])

    with col2:
        st.text(names[2])
        st.image(poster_paths[2])

    with col3:
        st.text(names[3])
        st.image(poster_paths[3])

    with col4:
        st.text(names[4])
        st.image(poster_paths[4])

    with col5:
        st.text(names[5])
        st.image(poster_paths[5])
