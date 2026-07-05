import streamlit as st
import pickle
import difflib
import requests
import urllib.parse
import concurrent.futures
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load data
@st.cache_resource
def load_data():
    movies_data = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies_data, similarity

movies_data, similarity = load_data()
list_of_all_titles = [str(t) for t in movies_data['title'].tolist()]

# Fetch single movie poster
@st.cache_data(show_spinner=False)
def get_movie_poster(title):
    try:
        query = urllib.parse.quote(title)
        url = f"https://imdb.iamidiotareyoutoo.com/search?q={query}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok") and data.get("description"):
                description = data["description"]
                for item in description:
                    item_title = item.get("#TITLE", "").lower()
                    if title.lower() in item_title or item_title in title.lower():
                        if item.get("#IMG_POSTER"):
                            return item["#IMG_POSTER"]
                if description[0].get("#IMG_POSTER"):
                    return description[0]["#IMG_POSTER"]
    except Exception:
        pass
    # High-quality fallback poster image from Unsplash
    return "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?auto=format&fit=crop&w=300&q=80"

# Fetch multiple movie posters in parallel
def fetch_posters_in_parallel(titles):
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(titles)) as executor:
        results = list(executor.map(get_movie_poster, titles))
    return results

# Custom CSS Injection for Rich Aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background-color: #0b0f19 !important;
    color: #f3f4f6 !important;
}

/* Glassmorphism selected movie container */
.selected-movie-container {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    margin-bottom: 2.5rem;
}

/* Genre tags */
.genre-tag {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 30px;
    padding: 0.25rem 0.75rem;
    font-size: 0.85rem;
    font-weight: 500;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}

/* Selected movie details styling */
.movie-title-large {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.movie-tagline {
    font-style: italic;
    color: #9ca3af;
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    font-weight: 300;
}

.meta-item {
    font-size: 0.95rem;
    color: #d1d5db;
    margin-bottom: 0.6rem;
}

.meta-label {
    font-weight: 600;
    color: #818cf8;
}

/* Premium Movie Cards Grid */
.rec-card {
    background: rgba(17, 24, 39, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 16px;
    padding: 0.8rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.rec-card:hover {
    transform: translateY(-8px);
    background: rgba(17, 24, 39, 0.85);
    border-color: rgba(139, 92, 246, 0.35);
    box-shadow: 0 12px 25px rgba(139, 92, 246, 0.18);
}

.card-img-container {
    width: 100%;
    aspect-ratio: 2/3;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    margin-bottom: 0.8rem;
}

.card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.rec-card:hover .card-img {
    transform: scale(1.06);
}

.rec-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f3f4f6;
    margin-bottom: 0.3rem;
    line-height: 1.3;
    height: 2.6rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.card-badge-container {
    display: flex;
    justify-content: center;
    gap: 8px;
    align-items: center;
    font-size: 0.75rem;
    color: #9ca3af;
}

.card-rating-badge {
    background: rgba(245, 158, 11, 0.12);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.25);
    padding: 0.1rem 0.4rem;
    border-radius: 6px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 2px;
}

/* Custom Search Box style */
div.stTextInput > div > div > input {
    background-color: rgba(17, 24, 39, 0.6) !important;
    color: #f3f4f6 !important;
    border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 30px !important;
    padding: 0.6rem 1.5rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
}

div.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.3) !important;
}

/* Submit recommendation button */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    color: white !important;
    border: none !important;
    padding: 0.6rem 2.2rem !important;
    font-weight: 600 !important;
    border-radius: 30px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    margin-top: 1rem;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    background: linear-gradient(135deg, #4f46e5, #9333ea) !important;
}

/* Expander custom look */
.streamlit-expanderHeader {
    background-color: rgba(17, 24, 39, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    color: #a5b4fc !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
    <h1 style="font-weight: 800; font-size: 3.2rem; background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.4rem; letter-spacing: -1.5px;">🎬 CineMatch</h1>
    <p style="color: #9ca3af; font-size: 1.15rem; font-weight: 300; letter-spacing: 0.5px;">Find your next movie experience using TF-IDF similarity</p>
</div>
""", unsafe_allow_html=True)

# Centered Search container
col_l, col_c, col_r = st.columns([1, 2, 1])

with col_c:
    movie_name = st.text_input(
        "", 
        placeholder="Search for a movie (e.g. Inception, Avatar, Iron Man, Interstellar)..."
    )
    submit_button = st.button("Generate Recommendations")

if submit_button or movie_name:
    if movie_name:
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, n=1, cutoff=0.4)

        if find_close_match:
            close_match = find_close_match[0]
            
            with st.spinner(f"Matching with '{close_match}' and calculating recommendations..."):
                # Get selected movie data
                movie_row = movies_data[movies_data.title == close_match].iloc[0]
                idx_of_movie = int(movie_row['index'])

                # Compute similarity recommendations
                similarity_score = list(enumerate(similarity[idx_of_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                # Get top 6 recommendations (excluding search movie)
                top_6_recs = []
                for item in sorted_similar_movies:
                    idx = item[0]
                    title_from_index = movies_data.iloc[idx]['title']
                    if title_from_index != close_match:
                        top_6_recs.append(idx)
                    if len(top_6_recs) == 6:
                        break

                # Get additional 24 recommendations
                other_recs = []
                for item in sorted_similar_movies:
                    idx = item[0]
                    title_from_index = movies_data.iloc[idx]['title']
                    if title_from_index != close_match and idx not in top_6_recs:
                        other_recs.append(idx)
                    if len(other_recs) == 24:
                        break

                # Fetch posters in parallel for selected movie + top 6 recommendations
                titles_to_fetch = [close_match] + [movies_data.iloc[i]['title'] for i in top_6_recs]
                posters = fetch_posters_in_parallel(titles_to_fetch)
                
                selected_poster = posters[0]
                rec_posters = posters[1:]

            # ---------------- SELECT MOVIES DISPLAY ----------------
            st.write("### 🎬 Matched Film")
            
            # Formatting fields
            genres = str(movie_row['genres']).split()
            tagline = str(movie_row['tagline']) if pd.notna(movie_row['tagline']) and str(movie_row['tagline']).strip() != "" else ""
            vote_avg = str(movie_row['vote_average']) if pd.notna(movie_row['vote_average']) else "N/A"
            runtime = str(movie_row['runtime']) if pd.notna(movie_row['runtime']) and str(movie_row['runtime']).strip() != "" else "N/A"
            release_date = str(movie_row['release_date'])
            year = release_date.split('-')[-1] if '-' in release_date else "N/A"
            overview = str(movie_row['overview']) if pd.notna(movie_row['overview']) else "No description available."
            director = str(movie_row['director']) if pd.notna(movie_row['director']) and str(movie_row['director']).strip() != "" else "Unknown"
            cast = str(movie_row['cast']).split() if pd.notna(movie_row['cast']) else []
            cast_display = ", ".join(cast[:3]) if cast else "Unknown"

            # Create a 2-column view for Selected Movie inside a custom styled container
            st.markdown('<div class="selected-movie-container">', unsafe_allow_html=True)
            m_col1, m_col2 = st.columns([1, 2.5])
            
            with m_col1:
                st.markdown(f'<img src="{selected_poster}" class="movie-poster-img" alt="{close_match}">', unsafe_allow_html=True)
                
            with m_col2:
                st.markdown(f'<div class="movie-title-large">{close_match}</div>', unsafe_allow_html=True)
                if tagline:
                    st.markdown(f'<div class="movie-tagline">"{tagline}"</div>', unsafe_allow_html=True)
                
                # Render Genre badges
                genre_html = "".join([f'<span class="genre-tag">{g}</span>' for g in genres if g])
                if genre_html:
                    st.markdown(genre_html, unsafe_allow_html=True)
                st.markdown('<div style="margin-bottom: 1.2rem;"></div>', unsafe_allow_html=True)
                
                # Metadata
                st.markdown(f'<div class="meta-item"><span class="card-rating-badge">⭐ {vote_avg}/10</span> &nbsp;|&nbsp; <span class="meta-label">Duration:</span> {runtime} min &nbsp;|&nbsp; <span class="meta-label">Released:</span> {year}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-item"><span class="meta-label">Director:</span> {director}</div>', unsafe_allow_html=True)
                if cast_display:
                    st.markdown(f'<div class="meta-item"><span class="meta-label">Starring:</span> {cast_display}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="margin-top: 1rem; line-height: 1.6; color: #e5e7eb; font-size: 1.05rem;">{overview}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.write("---")
            
            # ---------------- RECOMMENDATIONS DISPLAY ----------------
            st.write("### 🍿 Recommended For You")
            st.write("")
            
            rec_cols = st.columns(6)
            for i, idx in enumerate(top_6_recs):
                rec_row = movies_data.iloc[idx]
                r_title = rec_row['title']
                r_poster = rec_posters[i]
                r_vote = str(rec_row['vote_average']) if pd.notna(rec_row['vote_average']) else "N/A"
                r_date = str(rec_row['release_date'])
                r_year = r_date.split('-')[-1] if '-' in r_date else "N/A"
                
                with rec_cols[i]:
                    st.markdown(f"""
                    <div class="rec-card">
                        <div class="card-img-container">
                            <img src="{r_poster}" class="card-img" alt="{r_title}">
                        </div>
                        <div class="rec-title" title="{r_title}">{r_title}</div>
                        <div class="card-badge-container">
                            <span class="card-rating-badge">★ {r_vote}</span>
                            <span>•</span>
                            <span>{r_year}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.write("")
            st.write("")

            # ---------------- ADDITIONAL RECOMMENDATIONS ----------------
            with st.expander("🔍 Explore 24 More Similar Movies"):
                st.write("")
                # Show in a nice responsive bullet/grid layout
                cols_more = st.columns(3)
                for index_more, idx in enumerate(other_recs):
                    rec_row_more = movies_data.iloc[idx]
                    r_title_more = rec_row_more['title']
                    r_vote_more = str(rec_row_more['vote_average']) if pd.notna(rec_row_more['vote_average']) else "N/A"
                    r_date_more = str(rec_row_more['release_date'])
                    r_year_more = r_date_more.split('-')[-1] if '-' in r_date_more else "N/A"
                    
                    col_index = index_more % 3
                    with cols_more[col_index]:
                        st.markdown(f"**{index_more+7}. {r_title_more}** ({r_year_more}) — ⭐ {r_vote_more}/10")
                        
        else:
            st.warning("No close match found. Please try a different movie name.")
    else:
        st.warning("Please enter a movie name.")