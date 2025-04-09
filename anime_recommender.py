import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# Load the pickle file
def load_data():
    try:
        with open('anime_recommendations.pkl', 'rb') as f:
            data = pickle.load(f)
        st.write("Data loaded successfully!")
        return data
    except FileNotFoundError:
        st.error("Error: 'anime_recommendations.pkl' not found in the current directory. Please ensure the file is in the same folder as this script.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Recommendation function
def get_recommendations(title, cosine_sim, titles, genres):
    try:
        idx = titles.index(title)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get top 10 similar anime (excluding itself)
        anime_indices = [i[0] for i in sim_scores]
        return pd.DataFrame({
            'Title': [titles[i] for i in anime_indices],
            'Genre': [genres[i] for i in anime_indices]
        })
    except ValueException as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Streamlit app
def main():
    st.title("Anime Recommendation System")
    st.write("Search for an anime and get 10 recommendations based on genre similarity!")

    # Load data
    data = load_data()
    if data is None:
        st.stop()  # Stop execution if data loading fails

    titles = data['titles']
    genres = data['genres']
    cosine_sim = data['cosine_sim']

    # Debug: Display first few titles to verify data
    st.write("Sample titles:", titles[:5])

    # Search bar
    selected_anime = st.selectbox("Select an anime:", titles)

    if st.button("Get Recommendations"):
        # Show selected anime
        st.subheader(f"Selected Anime: {selected_anime}")
        selected_idx = titles.index(selected_anime)
        st.write(f"Genre: {genres[selected_idx]}")

        # Get and display recommendations
        st.subheader("Recommended Anime:")
        recommendations = get_recommendations(selected_anime, cosine_sim, titles, genres)
        if not recommendations.empty:
            st.table(recommendations)
        else:
            st.write("No recommendations available.")

if __name__ == '__main__':
    main()