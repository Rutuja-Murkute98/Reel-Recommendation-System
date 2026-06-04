from flask import Flask, render_template, request
import os
import pickle

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_SIMILARITY_PATH = os.path.join(MODELS_DIR, "user_similarity.pkl")
USER_REEL_MATRIX_PATH = os.path.join(MODELS_DIR, "user_reel_matrix.pkl")
REEL_DATA_PATH = os.path.join(DATA_DIR, "reel_recommendation_dataset_1000_rows.csv")


# ==========================
# HELPER FUNCTIONS TO LOAD / GENERATE MODELS
# ==========================

def generate_collaborative_models():
    """Generate collaborative filtering models from the CSV dataset."""
    if not os.path.exists(REEL_DATA_PATH):
        raise FileNotFoundError(f"Required dataset not found: {REEL_DATA_PATH}")

    print("Generating collaborative recommendation models...")
    df = pd.read_csv(REEL_DATA_PATH)

    df["interaction_score"] = (
        (df["watch_percentage"] * 0.1)
        + (df["liked"] * 3)
        + (df["shared"] * 5)
        + (df["saved"] * 4)
        + (df["clicked"] * 2)
        + (df["purchased"] * 10)
    )

    user_reel_matrix = df.pivot_table(
        index="user_id",
        columns="reel_id",
        values="interaction_score",
        fill_value=0,
    )

    user_similarity = cosine_similarity(user_reel_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity,
        index=user_reel_matrix.index,
        columns=user_reel_matrix.index,
    )

    os.makedirs(MODELS_DIR, exist_ok=True)

    with open(USER_SIMILARITY_PATH, "wb") as f:
        pickle.dump(user_similarity_df, f)

    with open(USER_REEL_MATRIX_PATH, "wb") as f:
        pickle.dump(user_reel_matrix, f)

    print("Collaborative recommendation models generated successfully.")
    return user_similarity_df, user_reel_matrix


def load_collaborative_models():
    """Load models from disk, or generate them if they are not committed."""
    if (
        not os.path.exists(USER_SIMILARITY_PATH)
        or not os.path.exists(USER_REEL_MATRIX_PATH)
    ):
        return generate_collaborative_models()

    with open(USER_SIMILARITY_PATH, "rb") as f:
        user_similarity_df = pickle.load(f)

    with open(USER_REEL_MATRIX_PATH, "rb") as f:
        user_reel_matrix = pickle.load(f)

    return user_similarity_df, user_reel_matrix


# ==========================
# LOAD MODELS
# ==========================

user_similarity_df, user_reel_matrix = load_collaborative_models()


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
