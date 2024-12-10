import pickle
import requests  # For fetching posters
import streamlit as st

# Load similarity matrix and movies DataFrame
similarity = pickle.load(open('similary.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))  # This should be a DataFrame

# Extract movie titles for the dropdown
movies_list = movies['title'].values

# Define TMDb API key and helper function to fetch posters
API_KEY = "cdab35d28e20dc1bd7e62f15e925ee2f"

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"  # Placeholder for missing posters

# Define the recommend function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

# Streamlit app
st.title('Movie Recommender System')

# Selectbox for movie selection
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies_list
)

# Recommend button
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    if recommendations:
        st.write("### Top 5 Recommended Movies:")
        for title, poster in zip(recommendations, posters):
            col1, col2 = st.columns([1, 3])  # Adjust column widths
            with col1:
                st.image(poster, width=150)  # Display poster
            with col2:
                st.write(title)
