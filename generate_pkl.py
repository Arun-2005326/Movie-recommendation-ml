import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading CSV...")
movies_data = pd.read_csv('movies.csv')

# Clean the dataset by filtering out corrupted rows (non-numeric indexes)
movies_data = movies_data[pd.to_numeric(movies_data['index'], errors='coerce').notna()]
movies_data['index'] = movies_data['index'].astype(int)
movies_data = movies_data.reset_index(drop=True)

# Same features as the Jupyter notebook
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

print("Processing features...")
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine features exactly like the notebook
combined_features = (
    movies_data['genres'] + ' ' +
    movies_data['keywords'] + ' ' +
    movies_data['tagline'] + ' ' +
    movies_data['cast'] + ' ' +
    movies_data['director']
)

print("Vectorizing with TF-IDF (same as Jupyter notebook)...")
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

print("Computing similarity matrix (this may take a moment)...")
similarity = cosine_similarity(feature_vectors)

print("Saving pkl files...")
pickle.dump(movies_data, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print(f"Done! Saved {len(movies_data)} movies.")
