# 🎬 Reel Recommendation Engine

A production-ready machine learning recommendation system designed for e-commerce platforms to recommend video reels and products to users. This system uses both **content-based filtering** and **collaborative filtering** approaches for intelligent, personalized recommendations.

---

## ✨ Features

- **Dual Recommendation Strategies:**
  - 📊 **Content-Based Filtering:** Recommends reels based on product features
  - 👥 **Collaborative Filtering:** Recommends based on user behavior and preferences
  
- **Real-Time Recommendations:** Fast API endpoints for instant recommendations
- **Dynamic Model Generation:** Large models generated on-demand to reduce deployment size
- **Web Interface:** User-friendly UI to test recommendations
- **Production-Ready:** Deployed on Render with Gunicorn server
- **Scalable Architecture:** Can handle growing user base and product catalog

---

## 🏗️ Project Structure

```
reel-recommendation-engine/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment configuration
├── build.sh                        # Build script for Render
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variables template
├── Procfile                        # Heroku-style process file
│
├── models/                         # Pre-trained ML models
│   ├── content_products.pkl        # Product features data
│   ├── content_similarity.pkl      # Content similarity matrix (auto-generated)
│   ├── user_reel_matrix.pkl        # User-reel interaction data
│   └── user_similarity.pkl         # User similarity matrix
│
├── templates/
│   └── index.html                  # Web UI template
│
├── static/
│   └── style.css                   # Styling for web interface
│
├── notebooks/                      # Jupyter notebooks for analysis
│   ├── 01_content_based.ipynb      # Content-based model development
│   └── 02_collaborative.ipynb      # Collaborative filtering development
│
└── data/                           # Dataset files
    └── products.csv                # Product database
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- Git

### Local Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Reel-Recommendation-System.git
   cd Reel-Recommendation-System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .\.venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Web Interface**
   - Open browser and go to: `http://localhost:5000`
   - Enter a user ID to get recommendations

---

## 📊 How It Works

### Content-Based Filtering
```
Product Features (Name, Category, Description)
           ↓
TF-IDF Vectorization
           ↓
Cosine Similarity Matrix
           ↓
Recommendations based on Similar Products
```

### Collaborative Filtering
```
User Interaction History (Views, Likes, Purchases)
           ↓
User-Reel Interaction Matrix
           ↓
User Similarity Calculation
           ↓
Find Similar Users
           ↓
Recommend Reels they liked
```

### Hybrid Approach (Used in Production)
- Combines both strategies
- Content-based for new users/products (cold-start problem)
- Collaborative for experienced users (personalization)
- Weighted averaging for final recommendations

---

## 🔧 API Endpoints

### Home Page
```
GET / 
POST /
```
- **Description:** Web interface for testing recommendations
- **Input:** User ID via form
- **Output:** List of recommended reels with similarity scores

### Recommendation API
```
GET /api/recommend/<user_id>
```
- **Description:** Get recommendations for a user
- **Parameters:** user_id (integer)
- **Response:** JSON with recommended reel IDs and scores

---

## 📚 Technologies Used

| Category | Technology |
|----------|------------|
| **Backend** | Flask 3.0.3 |
| **Machine Learning** | scikit-learn 1.4.2 |
| **Data Processing** | pandas 2.2.2, numpy 1.26.4 |
| **Server** | Gunicorn 22.0.0 |
| **Deployment** | Render |
| **Frontend** | HTML5, CSS3 |

---

## 🔄 Training the Models

### Content-Based Model
Run the Jupyter notebook to train:
```bash
jupyter notebook notebooks/01_content_based.ipynb
```

This generates:
- `content_products.pkl` - Product features
- `content_similarity.pkl` - Similarity matrix

### Collaborative Filtering Model
Run the Jupyter notebook to train:
```bash
jupyter notebook notebooks/02_collaborative.ipynb
```

This generates:
- `user_reel_matrix.pkl` - User interactions
- `user_similarity.pkl` - User similarity matrix

---

## 💾 Data Format

### Products CSV (data/products.csv)
```csv
product_id,name,category,description,price
1,Product A,Electronics,High-quality electronic device,99.99
2,Product B,Fashion,Comfortable clothing item,49.99
```

### User Interaction Matrix
- **Rows:** Users (user_0, user_1, ...)
- **Columns:** Reels (reel_0, reel_1, ...)
- **Values:** Interaction score (0-5)
  - 0 = Not interacted
  - 1-5 = Engagement level

---

## 📝 Project Status

- ✅ Content-based filtering implemented
- ✅ Collaborative filtering implemented
- ✅ Flask API developed
- ✅ Web interface created
- ✅ Deployed on Render
- ✅ Production-ready

---

---

## 🙏 Acknowledgments

- Dataset: E-commerce reel interaction data
- Framework: Flask
- ML Libraries: scikit-learn, pandas, numpy
- Deployment: Render

---

## 📧 Contact

For questions or support, please reach out through GitHub issues.

**Happy Recommending! 🚀**

