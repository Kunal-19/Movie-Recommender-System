import streamlit as st
import pickle
import requests

def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmIwNjI2ODdjZDNlOTgwMTU4MWUwZGNkNWY1NWEyOSIsInN1YiI6IjY1ZDQ4ZWQ4MDlkZGE0MDE4ODU4Mjc2NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.G8ofd6ccaq-2Yy04ZilnzlE9Jkbj7qaYC2WXIKfspNI"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load the pickled file
with open('movies.pkl', 'rb') as f:
    movies_list = pickle.load(f)

with open('similarity.pkl','rb') as f:
    similarity = pickle.load(f)


def fetch_similar_movies(name):

    # Convert input name to lowercase for comparison
    name = name.lower()

    # Get index of the movie in movies_list
    idx = movies_list[movies_list['title'] == name].index[0]

    # Sort and get indices of similar movies
    indices = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)[1:6]

    # Append titles and posters of similar movies to the list
    col = st.columns(3, gap='large')
    i = 0
    for index, _ in indices:
        title = movies_list.iloc[index]['title']
        words = title.split()
        capitalized_words = [words[0].capitalize()] + [word.capitalize() if word.lower()
                                                       not in ['the', 'a', 'an', 'and', 'but',
                                                               'or', 'for', 'nor', 'on', 'at',
                                                               'to', 'by', 'of', 'in',
                                                               'with'] else word.lower() for word
                                                       in words[1:]]
        capitalized_title = ' '.join(capitalized_words)

        with col[i%3]:
            st.image(fetch_posters(movies_list.iloc[index]['id']), caption=capitalized_title, width=200)
        i += 1


st.title('Movie Recommender System')

name = st.selectbox(
    label="Movie Name",
    options=movies_list['title']
)

if st.button(label='Recommend'):
    fetch_similar_movies(name)
