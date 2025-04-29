import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# Set background and style
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wallpapercave.com/wp/wp5128415.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #ffffff;
            text-align: center;
            font-size: 48px;
            text-shadow: 2px 2px 4px #000000;
        }
        .subheader {
            color: #eeeeee;
            font-size: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Load the pickle file
def load_data():
    try:
        with open('anime_recommendations.pkl', 'rb') as f:
            data = pickle.load(f)
        st.write("✅ Data loaded successfully!")
        return data
    except FileNotFoundError:
        st.error("❌ Error: 'anime_recommendations.pkl' not found in the current directory. Please ensure the file is in the same folder as this script.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
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
    except ValueError as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Streamlit app
def main():
    set_background()
    st.markdown('<div class="title">Anime Recommendation System 🎌</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Discover anime you might love based on your taste!</div>', unsafe_allow_html=True)

    # Load data
    data = load_data()
    if data is None:
        st.stop()

    titles = data['titles']
    genres = data['genres']
    cosine_sim = data['cosine_sim']

    with st.container():
        selected_anime = st.selectbox("🎞️ Select an anime title:", titles)

        if st.button("✨ Get Recommendations"):
            st.markdown(f"### ✅ Selected Anime: `{selected_anime}`")
            selected_idx = titles.index(selected_anime)
            st.write(f"**Genre:** {genres[selected_idx]}")

            st.markdown("### 🔮 Recommended Anime:")
            recommendations = get_recommendations(selected_anime, cosine_sim, titles, genres)
            if not recommendations.empty:
                st.dataframe(recommendations)
            else:
                st.warning("⚠️ No recommendations available. Try another anime.")

if __name__ == '__main__':
    main()
