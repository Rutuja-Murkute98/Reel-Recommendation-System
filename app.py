from flask import Flask, render_template, request
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ==========================
# HELPER FUNCTION TO GENERATE MODELS
# ==========================

def generate_content_similarity():
    """Generate content_similarity if it doesn't exist"""
    similarity_path = "models/content_similarity.pkl"
    
    if not os.path.exists(similarity_path):
        print("Generating content_similarity.pkl...")
        try:
            content_products = pickle.load(open("models/content_products.pkl", "rb"))
            content_products['features'] = (
                content_products['name'] + ' ' + 
                content_products['category'] + ' ' + 
                content_products['description']
            )
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            tfidf_matrix = vectorizer.fit_transform(content_products['features'])
            similarity = cosine_similarity(tfidf_matrix)
            
            with open(similarity_path, 'wb') as f:
                pickle.dump(similarity, f)
            print("✓ content_similarity.pkl generated successfully!")
            return similarity
        except Exception as e:
            print(f"Error generating similarity: {e}")
            return None
    else:
        return pickle.load(open(similarity_path, "rb"))

# ==========================
# LOAD MODELS
# ==========================

os.makedirs("models", exist_ok=True)

content_products = pickle.load(
    open("models/content_products.pkl", "rb")
)

content_similarity = generate_content_similarity()

user_similarity_df = pickle.load(
    open("models/user_similarity.pkl", "rb")
)

user_reel_matrix = pickle.load(
    open("models/user_reel_matrix.pkl", "rb")
)


# ==========================
# RECOMMENDATION FUNCTION
# ==========================

def recommend_reels(user_id, n_recommendations=5):

    similar_users = (
        user_similarity_df[user_id]
        .sort_values(ascending=False)[1:6]
    )

    recommended_reels = {}

    for similar_user, similarity_score in similar_users.items():

        reels_watched = user_reel_matrix.loc[similar_user]

        for reel_id, score in reels_watched.items():

            if score > 0:

                if reel_id not in recommended_reels:
                    recommended_reels[reel_id] = 0

                recommended_reels[reel_id] += (
                    score * similarity_score
                )

    recommended_reels = sorted(
        recommended_reels.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommended_reels[:n_recommendations]


# ==========================
# HOME PAGE
# ==========================

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    error = None

    if request.method == "POST":

        try:

            user_id = int(
                request.form["user_id"]
            )

            # Check User Exists
            if user_id not in user_similarity_df.columns:

                error = (
                    f"User ID {user_id} not found. "
                    f"Please enter a valid User ID."
                )

            else:

                recommendations = recommend_reels(
                    user_id
                )

        except Exception as e:

            error = str(e)

    return render_template(
        "index.html",
        recommendations=recommendations,
        error=error
    )


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)