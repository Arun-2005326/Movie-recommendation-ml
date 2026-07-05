# 🎬 CineMatch - Movie Recommendation System

CineMatch is a modern, interactive, content-based Movie Recommendation System. It combines machine learning text-processing techniques with a sleek, responsive, and visually stunning Streamlit web interface. 

The system recommends movies by analyzing similarities between key metadata fields like **genres**, **keywords**, **tagline**, **cast**, and **director**.

---

## 🌟 Key Features

*   **Premium Web UI**: Designed with glassmorphic cards, custom dark mode colors, modern Google typography (*Outfit*), smooth hover transitions, and micro-animations.
*   **Fuzzy Search Matching**: Powered by Python's `difflib` to find matches even if you make minor spelling errors.
*   **Dynamic Poster Fetching**: Uses concurrent multi-threading (`ThreadPoolExecutor`) to asynchronously pull and display movie posters from an IMDb search API in real-time.
*   **Multi-tier Results**: Highlights the top 6 closest movie recommendations, followed by 24 supplementary movie suggestions.

---

## ⚙️ Technical Details (How it Works)

1.  **Feature Combination**: Text features (`genres`, `keywords`, `tagline`, `cast`, `director`) are merged into a single metadata soup for each movie.
2.  **TF-IDF Vectorization**: Text blocks are converted into numerical feature vectors using `TfidfVectorizer` to calculate the relative importance of words.
3.  **Cosine Similarity**: Measures the cosine of the angle between two multi-dimensional vectors to determine similarity scores ranging from 0 (completely different) to 1 (identical).
4.  **Serialization**: The prepared dataframe and similarity matrix are stored as `.pkl` files using `pickle` for instant loading in the web app.

---

## 📂 Project Structure

```text
├── ML Jul 2024 Movie Recomendation.ipynb  # Jupyter notebook for exploratory data analysis & prototyping
├── app.py                                 # Main Streamlit web application
├── generate_pkl.py                        # Python script to regenerate pickle files from the CSV
├── movies.csv                             # Raw dataset containing movie metadata
├── movies.pkl                             # [LFS] Serialized movie dataset
├── similarity.pkl                         # [LFS] Serialized cosine similarity matrix (184 MB)
├── requirements.txt                       # Declared Python library dependencies
└── README.md                              # Project documentation
```

---

## 🚀 Getting Started

### 📋 Prerequisites
Make sure you have the following installed:
*   [Python 3.8+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/) and [Git LFS](https://git-lfs.com/) (Required to pull the large `similarity.pkl` file)

### 📥 1. Clone & Download
Since the repository contains large files tracked by Git LFS, clone the repository using:
```bash
git clone https://github.com/Arun-2005326/Movie-recommendation-ml.git
cd Movie-recommendation-ml
```
*If you already cloned it without Git LFS, retrieve the large files with:*
```bash
git lfs pull
```

### 📦 2. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### ⚡ 3. Run the App
Launch the Streamlit web application locally:
```bash
streamlit run app.py
```
Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser to experience CineMatch!

---

## 🔄 Re-Generating the Models (Optional)
If you update `movies.csv` and want to compute a new similarity matrix, simply run the generator script:
```bash
python generate_pkl.py
```
This will automatically compute the new cosine similarity matrix and overwrite `movies.pkl` and `similarity.pkl` with the updated datasets.

---

## 📝 License
This project is open-source and available for educational and personal use.
